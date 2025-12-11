"""
Seed Script for SkillTwin Demo Data
Run this to populate the database with sample educational content
"""

import asyncio
import httpx

BASE_URL = "http://localhost:8000/api/v1"

# Demo User Profile
DEMO_PROFILE = {
    "user_id": "demo_user_001",
    "name": "Demo Student",
    "email": "demo@skilltwin.ai",
    "grade_level": "undergraduate",
    "preferred_modality": "visual",
    "subjects": ["Physics", "Mathematics", "Computer Science"]
}

# Demo Concepts (Physics - Mechanics)
DEMO_CONCEPTS = [
    {
        "name": "Newton's First Law",
        "description": "An object at rest stays at rest and an object in motion stays in motion unless acted upon by an external force.",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Newton's Laws",
        "prerequisites": [],
        "difficulty_level": 2
    },
    {
        "name": "Newton's Second Law",
        "description": "Force equals mass times acceleration (F = ma). The acceleration of an object depends on the net force and its mass.",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Newton's Laws",
        "prerequisites": ["Newton's First Law"],
        "difficulty_level": 3
    },
    {
        "name": "Newton's Third Law",
        "description": "For every action, there is an equal and opposite reaction.",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Newton's Laws",
        "prerequisites": ["Newton's First Law"],
        "difficulty_level": 2
    },
    {
        "name": "Kinetic Energy",
        "description": "The energy an object possesses due to its motion. KE = (1/2)mv²",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Energy",
        "prerequisites": ["Newton's Second Law"],
        "difficulty_level": 3
    },
    {
        "name": "Potential Energy",
        "description": "Stored energy based on position or configuration. Gravitational PE = mgh",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Energy",
        "prerequisites": [],
        "difficulty_level": 2
    },
    {
        "name": "Conservation of Energy",
        "description": "Energy cannot be created or destroyed, only transformed from one form to another.",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Energy",
        "prerequisites": ["Kinetic Energy", "Potential Energy"],
        "difficulty_level": 4
    },
    {
        "name": "Momentum",
        "description": "The product of mass and velocity (p = mv). A measure of motion quantity.",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Momentum",
        "prerequisites": ["Newton's Second Law"],
        "difficulty_level": 3
    },
    {
        "name": "Conservation of Momentum",
        "description": "In a closed system, total momentum before and after collision remains constant.",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Momentum",
        "prerequisites": ["Momentum", "Newton's Third Law"],
        "difficulty_level": 4
    }
]

# Demo Academic Documents (Educational Content)
DEMO_DOCUMENTS = [
    {
        "title": "Introduction to Newton's Laws of Motion",
        "content": """Newton's Laws of Motion form the foundation of classical mechanics. 

**First Law (Law of Inertia):** An object at rest stays at rest, and an object in motion stays in motion with the same speed and direction, unless acted upon by an unbalanced force. This is why you feel pushed back when a car accelerates - your body wants to stay at rest!

**Second Law (F = ma):** The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass. If you push a shopping cart with the same force, an empty cart accelerates faster than a full one because it has less mass.

**Third Law (Action-Reaction):** For every action, there is an equal and opposite reaction. When you push against a wall, the wall pushes back with equal force. This is why rockets work - they push exhaust gases backward, and the gases push the rocket forward.

These three laws explain everything from why planets orbit the sun to how cars brake safely.""",
        "source_type": "textbook",
        "source_name": "Physics Fundamentals",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Newton's Laws",
        "grade_level": "undergraduate",
        "difficulty_level": 3
    },
    {
        "title": "Understanding Energy in Physics",
        "content": """Energy is the capacity to do work. In physics, we categorize energy into different forms:

**Kinetic Energy (KE):** The energy of motion. KE = ½mv². A car moving at 60 mph has more kinetic energy than the same car at 30 mph - in fact, it has 4 times more (since energy scales with velocity squared)!

**Potential Energy (PE):** Stored energy due to position or configuration.
- Gravitational PE = mgh (mass × gravity × height)
- A book on a high shelf has more gravitational PE than one on the floor
- Elastic PE is stored in stretched springs or rubber bands

**Conservation of Energy:** Energy cannot be created or destroyed, only converted from one form to another. When you drop a ball:
1. At the top: Maximum PE, zero KE
2. Falling: PE converts to KE
3. At bottom: Maximum KE, minimum PE

This principle is fundamental to understanding everything from roller coasters to power plants.""",
        "source_type": "textbook",
        "source_name": "Physics Fundamentals",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Energy",
        "grade_level": "undergraduate",
        "difficulty_level": 3
    },
    {
        "title": "Momentum and Collisions",
        "content": """Momentum is a measure of how hard it is to stop a moving object.

**Definition:** Momentum (p) = mass × velocity (p = mv)
- A truck moving slowly can have the same momentum as a car moving fast
- Momentum is a vector - it has both magnitude and direction

**Conservation of Momentum:** In a closed system (no external forces), total momentum is conserved.

**Types of Collisions:**
1. **Elastic Collision:** Both momentum AND kinetic energy are conserved. Example: billiard balls colliding.

2. **Inelastic Collision:** Momentum is conserved, but kinetic energy is NOT conserved (some converts to heat, sound, deformation). Example: car crash.

3. **Perfectly Inelastic:** Objects stick together after collision. Maximum KE is lost. Example: catching a ball.

**Real-world Applications:**
- Car safety (crumple zones extend collision time, reducing force)
- Rocket propulsion (momentum conservation)
- Sports (hitting a baseball, kicking a soccer ball)""",
        "source_type": "textbook",
        "source_name": "Physics Fundamentals",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Momentum",
        "grade_level": "undergraduate",
        "difficulty_level": 4
    },
    {
        "title": "Problem-Solving with Newton's Second Law",
        "content": """Applying F = ma to solve physics problems:

**Step-by-Step Approach:**
1. Draw a free-body diagram showing all forces
2. Choose a coordinate system
3. Write equations: ΣF = ma for each direction
4. Solve for unknowns

**Example 1: Simple Push**
A 10 kg box is pushed with 50 N force on a frictionless surface.
- F = ma
- 50 = 10 × a
- a = 5 m/s²

**Example 2: Inclined Plane**
A 5 kg block slides down a 30° frictionless incline.
- Forces: Weight (mg) down, Normal force perpendicular to surface
- Component along incline: mg sin(30°) = 5 × 10 × 0.5 = 25 N
- a = F/m = 25/5 = 5 m/s²

**Example 3: With Friction**
Same block with friction coefficient μ = 0.2:
- Friction force = μN = μ mg cos(30°) = 0.2 × 5 × 10 × 0.866 = 8.66 N
- Net force = 25 - 8.66 = 16.34 N
- a = 16.34/5 = 3.27 m/s²

**Common Mistakes to Avoid:**
- Forgetting to include all forces
- Wrong direction for friction (always opposes motion)
- Confusing mass and weight""",
        "source_type": "lecture_notes",
        "source_name": "Prof. Smith's Physics 101",
        "subject": "Physics",
        "topic": "Mechanics",
        "subtopic": "Newton's Laws",
        "grade_level": "undergraduate",
        "difficulty_level": 4
    },
    {
        "title": "Python Programming Basics",
        "content": """Introduction to Python programming for beginners.

**Variables and Data Types:**
```python
# Numbers
x = 10          # integer
y = 3.14        # float

# Strings
name = "SkillTwin"

# Lists
numbers = [1, 2, 3, 4, 5]

# Dictionaries
student = {"name": "John", "grade": 90}
```

**Control Flow:**
```python
# If statements
if score >= 90:
    print("A grade")
elif score >= 80:
    print("B grade")
else:
    print("Keep studying!")

# Loops
for i in range(5):
    print(i)

while count < 10:
    count += 1
```

**Functions:**
```python
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

result = calculate_average([85, 90, 78, 92])
print(f"Average: {result}")
```

**Key Concepts:**
- Python uses indentation for code blocks
- Variables don't need type declarations
- Lists are mutable, tuples are immutable
- Functions help organize and reuse code""",
        "source_type": "textbook",
        "source_name": "Python for Beginners",
        "subject": "Computer Science",
        "topic": "Programming",
        "subtopic": "Python Basics",
        "grade_level": "undergraduate",
        "difficulty_level": 2
    },
    {
        "title": "Calculus: Derivatives and Their Applications",
        "content": """Understanding derivatives in calculus.

**What is a Derivative?**
The derivative measures the rate of change of a function. If y = f(x), then dy/dx tells us how fast y changes as x changes.

**Notation:**
- f'(x) - Lagrange notation
- dy/dx - Leibniz notation
- d/dx[f(x)] - Operator notation

**Basic Rules:**
1. **Power Rule:** d/dx[x^n] = nx^(n-1)
   - d/dx[x³] = 3x²
   
2. **Constant Rule:** d/dx[c] = 0

3. **Sum Rule:** d/dx[f + g] = f' + g'

4. **Product Rule:** d/dx[fg] = f'g + fg'

5. **Chain Rule:** d/dx[f(g(x))] = f'(g(x)) × g'(x)

**Physics Applications:**
- Velocity = derivative of position: v = dx/dt
- Acceleration = derivative of velocity: a = dv/dt
- If position x = t³, velocity v = 3t², acceleration a = 6t

**Real-world Examples:**
- Rate of population growth
- Speed of chemical reactions
- Marginal cost in economics
- Slope of a curve at any point""",
        "source_type": "textbook",
        "source_name": "Calculus Essentials",
        "subject": "Mathematics",
        "topic": "Calculus",
        "subtopic": "Derivatives",
        "grade_level": "undergraduate",
        "difficulty_level": 4
    }
]

# Demo Student Context (Learning History)
DEMO_STUDENT_CONTEXTS = [
    {
        "content": "Student correctly solved F=ma problem: A 5kg object accelerated at 2 m/s². Calculated force as 10N.",
        "context_type": "answer",
        "concept_name": "Newton's Second Law",
        "subject": "Physics",
        "topic": "Mechanics",
        "was_correct": True
    },
    {
        "content": "Student asked: Why does a heavier object not fall faster than a lighter one?",
        "context_type": "question",
        "concept_name": "Newton's Second Law",
        "subject": "Physics",
        "topic": "Mechanics",
        "was_correct": None
    },
    {
        "content": "Student confused static and kinetic friction - thought kinetic friction is always greater.",
        "context_type": "misconception",
        "concept_name": "Newton's Laws",
        "subject": "Physics",
        "topic": "Mechanics",
        "was_correct": False
    },
    {
        "content": "Student successfully applied conservation of energy to calculate final velocity of falling object.",
        "context_type": "answer",
        "concept_name": "Conservation of Energy",
        "subject": "Physics",
        "topic": "Mechanics",
        "was_correct": True
    },
    {
        "content": "Student prefers visual explanations with diagrams and step-by-step problem solving.",
        "context_type": "note",
        "concept_name": None,
        "subject": "Physics",
        "topic": "General",
        "was_correct": None
    }
]


async def seed_database():
    """Seed the database with demo content"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("🌱 Starting database seeding...")
        
        # 1. Create Demo Profile
        print("\n📝 Creating demo learner profile...")
        try:
            response = await client.post(f"{BASE_URL}/ltp/profiles", json=DEMO_PROFILE)
            if response.status_code == 200:
                profile = response.json()
                profile_id = profile["id"]
                print(f"   ✅ Created profile: {profile_id}")
            else:
                # Try to get existing profile
                print(f"   ⚠️ Profile creation returned {response.status_code}, checking for existing...")
                response = await client.get(f"{BASE_URL}/ltp/profiles")
                if response.status_code == 200:
                    profiles = response.json()
                    if profiles:
                        profile_id = profiles[0]["id"]
                        print(f"   ✅ Using existing profile: {profile_id}")
                    else:
                        print("   ❌ No profiles found")
                        return
                else:
                    print(f"   ❌ Could not get profiles: {response.text}")
                    return
        except Exception as e:
            print(f"   ❌ Error creating profile: {e}")
            return
        
        # 2. Add Concepts
        print("\n📚 Adding educational concepts...")
        concept_ids = {}
        for concept in DEMO_CONCEPTS:
            try:
                response = await client.post(f"{BASE_URL}/ltp/concepts", json=concept)
                if response.status_code == 200:
                    result = response.json()
                    concept_ids[concept["name"]] = result["id"]
                    print(f"   ✅ Added: {concept['name']}")
                else:
                    print(f"   ⚠️ {concept['name']}: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error adding {concept['name']}: {e}")
        
        # 3. Add Academic Documents (for RAG)
        print("\n📖 Adding academic documents to knowledge base...")
        for doc in DEMO_DOCUMENTS:
            try:
                response = await client.post(f"{BASE_URL}/rag/documents", json=doc)
                if response.status_code == 200:
                    print(f"   ✅ Added: {doc['title']}")
                else:
                    print(f"   ⚠️ {doc['title']}: {response.status_code} - {response.text[:100]}")
            except Exception as e:
                print(f"   ❌ Error adding {doc['title']}: {e}")
        
        # 4. Add Student Context (Learning History)
        print("\n🧠 Adding student learning history...")
        for ctx in DEMO_STUDENT_CONTEXTS:
            try:
                response = await client.post(
                    f"{BASE_URL}/rag/contexts/{profile_id}",
                    json=ctx
                )
                if response.status_code == 200:
                    print(f"   ✅ Added context: {ctx['content'][:50]}...")
                else:
                    print(f"   ⚠️ Context: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error adding context: {e}")
        
        # 5. Set some initial mastery levels
        print("\n📊 Setting initial mastery levels...")
        mastery_updates = [
            ("Newton's First Law", 0.85),
            ("Newton's Second Law", 0.65),
            ("Kinetic Energy", 0.45),
            ("Potential Energy", 0.70),
        ]
        for concept_name, mastery in mastery_updates:
            if concept_name in concept_ids:
                try:
                    response = await client.put(
                        f"{BASE_URL}/ltp/mastery/{concept_ids[concept_name]}",
                        json={
                            "profile_id": profile_id,
                            "mastery_level": mastery,
                            "interaction_type": "practice",
                            "was_correct": True
                        }
                    )
                    if response.status_code == 200:
                        print(f"   ✅ {concept_name}: {mastery*100:.0f}% mastery")
                except Exception as e:
                    print(f"   ❌ Error updating mastery: {e}")
        
        print("\n" + "="*60)
        print("🎉 Database seeding complete!")
        print("="*60)
        print(f"\n📋 Demo Profile ID: {profile_id}")
        print("\n🧪 You can now test the AI with queries like:")
        print('   - "Explain Newton\'s Second Law"')
        print('   - "What is kinetic energy?"')
        print('   - "How does momentum conservation work?"')
        print('   - "Solve an F=ma problem for me"')
        print(f"\n🌐 API Docs: http://localhost:8000/docs")
        print(f"🖥️  Frontend: http://localhost:8080")


if __name__ == "__main__":
    asyncio.run(seed_database())
