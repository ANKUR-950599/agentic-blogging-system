import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "agentic_blogging_system")

async def seed_personas():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    personas = [
        {
            "name": "The Career-Crossroads Undergrad",
            "category": "2nd–3rd year undergrad — BTech / BBA / BCom Honours / BCA / BSc / BA",
            "age": 20,
            "location": "Kolkata",
            "layers": {
                "pain_points": [
                    "Degree curriculum feels outdated vs. what LinkedIn job descriptions demand.",
                    "No clarity on which specialization within their field actually leads to a job (data analyst vs. business analyst vs. product analyst).",
                    "Internship hunt is brutal — unpaid offers, ghosted applications, nepotism in shortlists.",
                    "Peer comparison amplified by LinkedIn — every classmate seems to be 'thrilled to announce.'",
                    "Tier-2/3 college students struggle to get past resume screening at top firms.",
                    "Genuine confusion between higher studies (MBA, MS, MA), government exams, and direct private placement.",
                    "Multiple half-finished online courses; certificate fatigue without skill consolidation.",
                    "CGPA pressure clashing with project/internship time.",
                    "Family pressure to 'settle' via WBCS, SSC, or banking exams alongside private aspirations.",
                    "Financial dependence on parents creates guilt around spending on premium courses.",
                    "Public speaking and English communication gaps surface in interviews and case competitions.",
                    "Burnout from juggling college + side hustles + exam prep + social life.",
                    "Uncertainty about whether to stay in Kolkata for the first job or migrate for higher salary."
                ],
                "goals": [
                    "Land a paid internship in 2nd/3rd year that converts to a PPO or strong resume line.",
                    "Build one demonstrable skill stack — data analytics, full-stack, digital marketing, UX, finance modeling, content.",
                    "Crack campus placements or first off-campus role at ₹4–8 LPA range.",
                    "Get into a respected MBA/MS/PG program as a parallel safety net.",
                    "Build a public portfolio — GitHub, Behance, Medium, LinkedIn — that compensates for college tier.",
                    "Develop a clear 2-year career narrative they can defend in interviews.",
                    "Achieve some financial independence — freelancing, paid projects, tutoring.",
                    "Network beyond their immediate college bubble.",
                    "Improve spoken English and interview confidence.",
                    "Make an informed bet between private sector, government job track, and entrepreneurship."
                ],
                "fears": [
                    "Graduating without a job offer and joining the 'unemployed graduate' statistic.",
                    "Being trapped in a low-paying BPO or non-core role after a technical degree.",
                    "Watching peers from 'better' colleges leapfrog them despite equal ability.",
                    "Investing in a course/specialization that becomes obsolete or oversaturated.",
                    "Disappointing parents who funded the degree expecting clear ROI.",
                    "Permanent migration away from Kolkata and the emotional cost.",
                    "Failing competitive exams (CAT, GATE, GRE, WBCS) after years of side preparation.",
                    "Mental health deterioration — anxiety, sleep loss, comparison spirals.",
                    "Being 'average' — neither placed in a top firm nor cracking an elite exam."
                ],
                "psychology": [
                    "Outcome-obsessed — every action is filtered through 'will this help me get placed?'",
                    "Comparison-saturated — LinkedIn scrolling produces both motivation and despair.",
                    "Trial-and-error learner — willing to start a course, abandon it, try the next.",
                    "Community-seeking — joins Discord servers, Telegram groups, Reddit threads for validation.",
                    "Quietly ambitious — won't always voice big dreams aloud, but tracks them obsessively.",
                    "Pragmatic over passionate — chooses career paths by market demand, not pure interest.",
                    "Skeptical of marketing — values raw, unpolished content from working professionals.",
                    "Time-anxious — feels every semester is a closing window.",
                    "Identity-rebuilding — actively shedding 'student' identity, performing 'professional.'",
                    "Bilingual operator — codes in English, thinks in Bangla, networks in Hindi when needed."
                ]
            }
        },
        {
            "name": "The Mid-Career Transitioner",
            "category": "Working professional (4–7 years experience)",
            "age": 29,
            "location": "Kolkata",
            "layers": {
                "pain_points": [
                    "Salary stagnation — 8–10% annual hikes vs. 40–80% jumps available via switch.",
                    "Role has become repetitive; learning curve flattened after year 2–3.",
                    "Skill set increasingly outdated — manual testing, legacy stacks, basic Excel reporting when market wants automation, cloud, SQL/Python, GenAI literacy.",
                    "Imposter syndrome when interviewing at product companies or GCCs.",
                    "Switch anxiety — fear of joining a worse company and losing notice-period leverage.",
                    "Family responsibilities — parents' health, spouse's career, child planning — limit risk-taking.",
                    "Time scarcity — 10–11 hours including commute leaves 1–2 hours for upskilling.",
                    "Information overload — every LinkedIn influencer recommends a different path (data, product, cloud, GenAI, MBA, PMP).",
                    "Visible salary gap with cousins/college batchmates who migrated to Bangalore/Hyderabad/Pune.",
                    "Manager bottleneck — limited internal mobility, slow promotion cycles.",
                    "Pressure to relocate vs. emotional cost of leaving Kolkata-based family.",
                    "Cost of premium upskilling programs (₹50k–₹3L) feels like a real financial decision, not a casual purchase.",
                    "Mental health strain — Sunday-night dread, weekend burnout, no clear off-ramp."
                ],
                "goals": [
                    "Achieve a 40%+ salary jump in the next switch, ideally to a product company, GCC, or specialized role.",
                    "Build a hireable skill stack — data engineering, cloud (AWS/Azure), product management, full-stack, GenAI/LLM, finance + analytics, or domain specialization.",
                    "Stay in Kolkata if possible; if not, optimize the relocation decision financially.",
                    "Build a strong LinkedIn presence and a network outside the current company.",
                    "Move from 'doer' to 'owner' — lead a project, mentor juniors, get visibility.",
                    "Decide between an executive MBA (IIM-C, ISB part-time, XLRI VIL) and direct upskilling.",
                    "Stabilize finances — clear high-interest debt, build emergency fund, start SIPs.",
                    "Create a clear 5-year plan with a defensible career narrative.",
                    "Find a manager and team where they can actually grow.",
                    "Reclaim some life — health, relationships, hobbies — without sabotaging the career."
                ],
                "fears": [
                    "Getting laid off in the next services-sector cost-cutting cycle.",
                    "Switching into a role they're under-qualified for and getting fired in probation.",
                    "Being permanently labeled 'service-company resource' by product-company recruiters.",
                    "Falling behind on AI/GenAI literacy and becoming obsolete.",
                    "Family expectations — marriage, child, home loan — colliding with career experimentation.",
                    "Spending heavily on a course/MBA that doesn't deliver ROI.",
                    "Burnout-driven quit without a backup plan.",
                    "Salary expectation getting locked low because of current CTC anchor.",
                    "Health issues from sedentary work, commute, and stress.",
                    "Looking back at 35 and realizing they played it too safe."
                ],
                "psychology": [
                    "Risk-aware, not risk-averse — willing to bet, but only after thorough due diligence.",
                    "ROI-driven — every learning hour and every rupee gets evaluated against career payoff.",
                    "Quietly disillusioned — public optimism, private fatigue.",
                    "Network-anxious — knows networking matters, finds it draining and inauthentic.",
                    "Outcome-led learner — won't learn for curiosity; learns for the next role.",
                    "Family-anchored — major decisions filtered through spouse, parents, financial obligations.",
                    "Brand-sensitive — values IIM/ISB/Scaler/Coursera-of-recognized-university-tag as resume signals.",
                    "Time-protective — guards weekends, resents low-value calls and generic webinars.",
                    "Skeptical — has seen too many 'career transformation' pitches to trust easily.",
                    "Identity-recalibrating — quietly asking 'what should I be known for by 35?'"
                ]
            }
        },
        {
            "name": "The Crossroads Freshman",
            "category": "Class 12th Passed (Post-Boards / Pre-College)",
            "age": 18,
            "location": "Kolkata",
            "layers": {
                "pain_points": [
                    "The Admission Limbo: The agonizing wait for centralized admission portals (WB-CAP) and merit lists while peers in other states have already started their sessions.",
                    "Cutoff Traps: Scoring a 'decent' 85–90% but realizing it's insufficient for the 'Big Three' (St. Xavier’s, Jadavpur, Presidency) in preferred honors subjects.",
                    "Entrance Fatigue: Mental burnout after 2 years of the 'Dummy School + Coaching' cycle (JEE/NEET/WBJEE/CUET) with no gap month to recover.",
                    "The 'Science vs. Passion' Conflict: Pressure to take core Science/Engineering when they are secretly interested in Design, Liberal Arts, or BCA/BBA.",
                    "Information Asymmetry: Overwhelmed by 'New Age' career options (AI, Data Science, Digital Marketing) vs. parents' 'Stable Degree' (B.Com/B.Sc/B.Tech) advice.",
                    "Kolkata Infrastructure Doubt: Wondering if staying in Kolkata for a degree will make them 'less hireable' than those going to Bangalore, Delhi, or Pune.",
                    "English Fluency Gap: Fear that their 'Bengali-medium' or 'Conversational English' won't survive the elite case competitions or GDs of top-tier colleges.",
                    "The Tuition Loop: Realizing that even after school ends, college will likely involve 'Private Tutors' for every semester to maintain a high CGPA.",
                    "Skill-Void Certification: Having a high board percentage but zero 'real-world' skills like coding, public speaking, or professional networking.",
                    "Commute Anxiety: The reality of a 1.5-hour journey (Bus/Metro/Auto) to North or South Kolkata colleges in the humid heat.",
                    "Social Media 'Achievement' Pressure: Seeing Instagram/LinkedIn posts of seniors with high-paying internships, creating a feeling of 'already being behind.'",
                    "Financial Guilt: Knowing the family is ready to spend ₹5L–₹10L for a private college but feeling they haven't 'earned' that investment via their rank."
                ],
                "goals": [
                    "The 'Safe Landing': Secure a seat in a reputable Kolkata college that has a 'brand name' recognizable to HRs.",
                    "Immediate Skill-Up: Learn one high-income skill (Python, UX Design, Content Writing) during the 3-month gap before college starts.",
                    "The 'PPO' Dream: Join a college that has a track record of placements at ₹5 LPA+ so the ROI is clear from Day 1.",
                    "Financial Micro-Independence: Earn ₹5k–₹10k/month through freelancing, tutoring, or campus ambassador roles.",
                    "Professional Identity: Transition from 'Student' to 'Professional' by cleaning up their social media and building a LinkedIn profile.",
                    "The 'Migration Safety Net': Build a profile strong enough to get a Tier-1 Master’s (MBA/MS) outside Bengal if the local job market fails.",
                    "Networking Beyond Adda: Join a community (Discord/Tech Clubs/Rotaract) that connects them with professionals outside their immediate neighborhood.",
                    "Communication Mastery: Become fluent and confident in English to 'crack' interviews at GCCs or Big 4 firms later.",
                    "Portfolio Building: Move beyond certificates to building 'Proof of Work' (GitHub repos, Behance portfolios, or published articles).",
                    "The Clear Roadmap: Find a mentor who can tell them exactly what to do for the next 3 years to avoid being 'just another graduate.'"
                ],
                "fears": [
                    "The 'General Line' Stigma: Fear that taking a B.A./B.Sc. Honors will lead to a dead-end 'Government Exam' loop for 5 years.",
                    "The 'Home-Grown' Disadvantage: Fearing that staying in Kolkata for college makes them 'soft' and less competitive than hostel-dwelling peers.",
                    "Degree Obsolescence: Spending 4 years on a syllabus that AI or automation renders useless by graduation (2029-2030).",
                    "Parental Disappointment: Seeing the 'Result Day' joy fade into 'Admission Stress' if they don't get the 'Expected' college.",
                    "The 'Jobless Graduate' Tag: Ending up in a ₹15k BPO job despite having a 90% in Class 12.",
                    "Social Isolation: Seeing all close friends move to other cities for 'better opportunities,' leaving them alone in the city.",
                    "The 'Oversaturated' Field: Choosing CSE or BBA because everyone else is, only to find a 1:1000 candidate-to-job ratio later.",
                    "Mental Health Spiral: The 'Sunday Night Dread' shifting into 'Daily Existential Crisis' during the long admission wait.",
                    "Missing the 'Golden Window': Feeling that if they don't choose the 'Right' specialization now, their entire 40-year career is ruined.",
                    "Health Decline: Sedentary lifestyle from 2 years of 'Coaching-Home-School' continuing into college life."
                ],
                "psychology": [
                    "Outcome-Vigilant: They don't value 'knowledge for knowledge's sake.' They value 'knowledge for placement's sake.'",
                    "Comparison-Saturated: Every decision is benchmarked against 'What is the topper from my school doing?'",
                    "Skeptical of Traditional Authority: They trust a 22-year-old YouTuber/Influencer's career roadmap more than a 50-year-old Professor's advice.",
                    "Community-Dependent: They feel safer making career choices if 500 other people on a Telegram group are doing the same.",
                    "The 'Middle-Class Hero' Complex: Obsessed with 'breaking out' of the middle-class struggle but terrified of the risk involved.",
                    "Bilingual Paradox: They consume high-end English content (Netflix/Tech-Twitter) but feel most emotionally connected to career advice delivered in 'Hinglish' or 'Bonglish.'",
                    "Time-Compressed: They feel 18 is 'late' to start a career; they want 'Success' by 22.",
                    "Pragmatic Pessimism: They assume the system is 'rigged' (nepotism/reservation) and thus look for 'loopholes' or 'hacks' to get ahead.",
                    "Brand-Sensitive: They will choose a worse course in a 'Famous College' over a better course in a 'New College.'",
                    "Validation-Seeker: Needs constant reassurance that 'it’s okay' to not have a clear plan yet, while simultaneously searching for one obsessively."
                ]
            }
        }
    ]

    # Delete existing data and insert the fresh seed
    await db.biopersonas.delete_many({})
    await db.biopersonas.insert_many(personas)
    print(f"✅ Successfully seeded {len(personas)} detailed Kolkata personas into {DB_NAME}.")

if __name__ == "__main__":
    asyncio.run(seed_personas())