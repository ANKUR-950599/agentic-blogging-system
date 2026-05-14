import os
import asyncio
import webbrowser
import logging
from motor.motor_asyncio import AsyncIOMotorClient

# Import your agents
from research_agent import UnifiedResearchAgent
from competitor_agent import CompetitorGapAgent
from author_agent import StrategicBlogAuthorAgent
from seo_agent import SEOMetadataAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("SmartPipeline")

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "agentic_blogging_system"
SITE_FOLDER = "my_blog_site"

async def check_if_research_needed():
    """Checks MongoDB to see if the competitor strategy queue is empty."""
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    # Looks for a strategy that hasn't been turned into a post yet
    pending_strategy = await db.competitor_gap_strategies.find_one({"post_status": {"$exists": False}})
    return pending_strategy is None # Returns True if empty

async def generate_html_site():
    """Converts MongoDB JSON posts into the HTML website folder."""
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    os.makedirs(SITE_FOLDER, exist_ok=True)
    
    style = """
    <style>
        body { font-family: 'Segoe UI', sans-serif; line-height: 1.7; max-width: 850px; margin: 0 auto; padding: 40px 20px; color: #333; background-color: #f4f7f9; }
        .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 30px; }
        h1 { color: #2c3e50; font-size: 2.5em; margin-bottom: 10px; }
        .meta { color: #95a5a6; font-size: 0.85em; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #eee; padding-bottom: 15px; margin-bottom: 25px; }
        h2 { color: #2980b9; margin-top: 40px; border-left: 5px solid #2980b9; padding-left: 15px; }
        .introduction { font-size: 1.1em; color: #34495e; border-bottom: 1px solid #f0f0f0; padding-bottom: 20px; margin-bottom: 20px; }
        .cta-section { background: #eef7fe; padding: 30px; border-radius: 8px; margin-top: 50px; border: 1px solid #3498db; }
        .cta-header { font-weight: bold; color: #2980b9; display: block; margin-bottom: 10px; font-size: 1.2em; }
        nav { margin-bottom: 30px; font-weight: bold; }
        nav a { text-decoration: none; color: #2980b9; }
        .home-list { list-style: none; padding: 0; }
        .home-list li { background: white; padding: 25px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); transition: 0.2s; }
        .home-list li:hover { transform: translateY(-3px); }
        .home-list a { font-size: 1.4em; color: #2c3e50; text-decoration: none; font-weight: bold; }
    </style>
    """

    index_html = f"<html><head>{style}<title>The Agentic Architect</title></head><body><h1>Strategic Content Pipeline</h1><ul class='home-list'>"

    cursor = db.strategic_blog_posts.find({}).sort("created_at", -1)
    async for post in cursor:
        slug = post.get('slug', 'post-' + str(post['_id']))
        filename = f"{slug}.html"
        
        blog_content = f"""<html><head>{style}<title>{post['title']}</title></head>
        <body>
            <nav><a href="index.html">← Back to Dashboard</a></nav>
            <div class="container">
                <h1>{post['title']}</h1>
                <div class="meta">Narrative: {post.get('narrative_framework', 'Strategic')} | Signal: High</div>
                <div class="introduction">{post.get('introduction', '')}</div>
        """
        
        for section in post.get('body_sections', []):
            blog_content += f"<section><h2>{section.get('header', '')}</h2><p>{section.get('content', '')}</p></section>"
        
        blog_content += f"""
                <div class="cta-section">
                    <span class="cta-header">Strategic Takeaway</span>
                    {post.get('strategic_cta', '')}
                </div>
            </div>
        </body></html>"""

        with open(os.path.join(SITE_FOLDER, filename), "w", encoding="utf-8") as f:
            f.write(blog_content)
        
        index_html += f'<li><a href="{filename}">{post["title"]}</a><br><small>{post.get("meta_description", "")[:120]}...</small></li>'

    index_html += "</ul></body></html>"
    with open(os.path.join(SITE_FOLDER, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

async def main():
    logger.info("🧠 Checking database state...")
    queue_is_empty = await check_if_research_needed()

    if queue_is_empty:
        logger.info("⚠️ Queue is empty! Triggering deep research cycle...")
        # Step A: Generate new research
        researcher = UnifiedResearchAgent()
        await researcher.run()
        
        # Step B: Generate new strategies
        competitor = CompetitorGapAgent()
        await competitor.run_massive_analysis()
    else:
        logger.info("✅ Database has pending topics. Skipping research phase.")

    # Step C & D: Author and SEO (These always run to consume the queue)
    logger.info("✍️ Triggering Author Agent...")
    author = StrategicBlogAuthorAgent()
    await author.run()

    logger.info("🔍 Triggering SEO Agent...")
    seo = SEOMetadataAgent()
    await seo.run()

    # Step E: Build and Deploy
    logger.info("🏗️ Generating HTML site...")
    await generate_html_site()

    logger.info("✅ Pipeline Complete! Opening tools...")
    os.startfile(os.path.abspath(SITE_FOLDER))
    webbrowser.open("https://app.netlify.com/drop")

if __name__ == "__main__":
    asyncio.run(main())