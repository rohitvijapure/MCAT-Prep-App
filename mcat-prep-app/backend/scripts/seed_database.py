#!/usr/bin/env python3
"""
Database seeding script for MCAT Prep application
Run this after migrations to populate the database with initial data
"""
import sys
import os
from datetime import date

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.core.security import get_password_hash
from app.models import (
    User,
    AAMCFoundationalConcept,
    Topic,
    StudyModule,
    Question,
)
import uuid

def seed_database():
    """Seed the database with initial data"""
    db = SessionLocal()

    try:
        print("🌱 Starting database seed...")

        # Create demo user
        print("Creating demo user...")
        demo_user = User(
            email="demo@mcatprep.com",
            password_hash=get_password_hash("demo123"),
            full_name="Demo Student",
            target_mcat_score=515,
            target_exam_date=date(2026, 4, 15),
            is_active=True,
        )
        db.add(demo_user)
        db.commit()
        print(f"✅ Created demo user: {demo_user.email} (password: demo123)")

        # AAMC Foundational Concepts - CPBS Section
        print("\nCreating AAMC foundational concepts...")
        concepts = [
            {
                "concept_code": "1A",
                "mcat_section": "CPBS",
                "title": "Structure and Function of Proteins and Their Constituent Amino Acids",
                "description": "Amino acid structure, protein structure and function",
            },
            {
                "concept_code": "1B",
                "mcat_section": "CPBS",
                "title": "Transmission of Genetic Information",
                "description": "DNA and gene expression",
            },
            {
                "concept_code": "4A",
                "mcat_section": "CPBS",
                "title": "Translational Motion, Forces, Work, Energy, and Equilibrium",
                "description": "Newtonian mechanics and energy",
            },
            {
                "concept_code": "5A",
                "mcat_section": "CPBS",
                "title": "Unique Nature of Water and Its Solutions",
                "description": "Water properties, pH, buffers",
            },
            {
                "concept_code": "5B",
                "mcat_section": "CPBS",
                "title": "Nature of Molecules and Intermolecular Interactions",
                "description": "Bonding, intermolecular forces",
            },
            # BBLS concepts
            {
                "concept_code": "1A",
                "mcat_section": "BBLS",
                "title": "Structure and Functions of Proteins",
                "description": "Protein structure, enzyme catalysis",
            },
            {
                "concept_code": "2A",
                "mcat_section": "BBLS",
                "title": "Assemblies of Molecules, Cells, and Groups of Cells",
                "description": "Cell structure and function",
            },
            # PSBB concepts
            {
                "concept_code": "6A",
                "mcat_section": "PSBB",
                "title": "Sensing the Environment",
                "description": "Sensory processing",
            },
            {
                "concept_code": "7A",
                "mcat_section": "PSBB",
                "title": "Individual Influences on Behavior",
                "description": "Personality, motivation",
            },
        ]

        concept_objects = []
        for concept_data in concepts:
            concept = AAMCFoundationalConcept(**concept_data)
            db.add(concept)
            concept_objects.append(concept)
        db.commit()
        print(f"✅ Created {len(concepts)} AAMC foundational concepts")

        # Topics
        print("\nCreating topics...")
        topics = [
            {
                "name": "Amino Acids and Proteins",
                "mcat_section": "CPBS",
                "foundational_concept_id": concept_objects[0].id,
                "description": "Structure and function of amino acids and proteins",
                "difficulty_level": 2,
            },
            {
                "name": "Thermodynamics and Energy",
                "mcat_section": "CPBS",
                "foundational_concept_id": concept_objects[2].id,
                "description": "Laws of thermodynamics, Gibbs free energy",
                "difficulty_level": 3,
            },
            {
                "name": "Acids and Bases",
                "mcat_section": "CPBS",
                "foundational_concept_id": concept_objects[3].id,
                "description": "pH, pKa, buffers, titrations",
                "difficulty_level": 2,
            },
            {
                "name": "Chemical Bonding",
                "mcat_section": "CPBS",
                "foundational_concept_id": concept_objects[4].id,
                "description": "Ionic, covalent, and metallic bonding",
                "difficulty_level": 2,
            },
            {
                "name": "Cell Biology",
                "mcat_section": "BBLS",
                "foundational_concept_id": concept_objects[6].id,
                "description": "Cell organelles and their functions",
                "difficulty_level": 2,
            },
        ]

        topic_objects = []
        for topic_data in topics:
            topic = Topic(**topic_data)
            db.add(topic)
            topic_objects.append(topic)
        db.commit()
        print(f"✅ Created {len(topics)} topics")

        # Study Modules
        print("\nCreating study modules...")
        study_modules = [
            {
                "title": "Introduction to Amino Acids",
                "mcat_section": "CPBS",
                "topic_id": topic_objects[0].id,
                "content_type": "text",
                "content": {
                    "summary": "Amino acids are the building blocks of proteins. There are 20 standard amino acids, each with unique side chains that determine their properties.",
                    "key_points": [
                        "All amino acids have an amino group, carboxyl group, and unique R group",
                        "Amino acids are classified as nonpolar, polar, acidic, or basic",
                        "At physiological pH, amino acids exist as zwitterions",
                    ],
                },
                "order_index": 1,
                "estimated_time_minutes": 15,
            },
            {
                "title": "Thermodynamics Fundamentals",
                "mcat_section": "CPBS",
                "topic_id": topic_objects[1].id,
                "content_type": "text",
                "content": {
                    "summary": "Thermodynamics describes energy transformations in chemical and physical processes.",
                    "key_points": [
                        "First Law: Energy is conserved",
                        "Second Law: Entropy of universe increases",
                        "Gibbs free energy predicts spontaneity: ΔG = ΔH - TΔS",
                    ],
                },
                "order_index": 1,
                "estimated_time_minutes": 20,
            },
            {
                "title": "pH and Buffers",
                "mcat_section": "CPBS",
                "topic_id": topic_objects[2].id,
                "content_type": "text",
                "content": {
                    "summary": "pH measures acidity/basicity of solutions. Buffers resist pH changes.",
                    "key_points": [
                        "pH = -log[H+]",
                        "Henderson-Hasselbalch equation: pH = pKa + log([A-]/[HA])",
                        "Buffers work best within ±1 pH unit of pKa",
                    ],
                },
                "order_index": 1,
                "estimated_time_minutes": 18,
            },
        ]

        for module_data in study_modules:
            module = StudyModule(**module_data)
            db.add(module)
        db.commit()
        print(f"✅ Created {len(study_modules)} study modules")

        # Sample Questions
        print("\nCreating sample questions...")
        questions = [
            {
                "id": uuid.uuid4(),
                "question_type": "standalone",
                "mcat_section": "CPBS",
                "topic_id": topic_objects[0].id,
                "foundational_concept_id": concept_objects[0].id,
                "difficulty_level": 2,
                "question_text": "Which of the following amino acids is most likely to be found in the interior of a folded protein?",
                "options": {
                    "A": "Glutamic acid",
                    "B": "Lysine",
                    "C": "Leucine",
                    "D": "Serine",
                },
                "correct_answer": "C",
                "correct_explanation": "Leucine is a nonpolar, hydrophobic amino acid. In aqueous environments, proteins fold such that hydrophobic residues are buried in the interior, away from water, while hydrophilic residues are on the surface.",
                "incorrect_explanations": {
                    "A": "Glutamic acid is acidic and hydrophilic, typically found on protein surfaces.",
                    "B": "Lysine is basic and hydrophilic, typically found on protein surfaces.",
                    "D": "Serine is polar and hydrophilic, typically found on protein surfaces.",
                },
                "tags": ["amino acids", "protein structure", "hydrophobic"],
                "estimated_time_seconds": 90,
            },
            {
                "id": uuid.uuid4(),
                "question_type": "standalone",
                "mcat_section": "CPBS",
                "topic_id": topic_objects[1].id,
                "foundational_concept_id": concept_objects[2].id,
                "difficulty_level": 3,
                "question_text": "A reaction has ΔH = -50 kJ/mol and ΔS = -100 J/(mol·K). At what temperature will the reaction become non-spontaneous?",
                "options": {
                    "A": "Below 500 K",
                    "B": "Above 500 K",
                    "C": "Below 250 K",
                    "D": "Above 250 K",
                },
                "correct_answer": "B",
                "correct_explanation": "For spontaneity, ΔG < 0. Using ΔG = ΔH - TΔS, we need -50,000 - T(-100) < 0. This simplifies to T < 500 K. Therefore, the reaction is spontaneous below 500 K and non-spontaneous above 500 K.",
                "incorrect_explanations": {
                    "A": "This is when the reaction IS spontaneous, not non-spontaneous.",
                    "C": "Incorrect calculation; remember to convert ΔS to kJ.",
                    "D": "Incorrect calculation of the crossover temperature.",
                },
                "tags": ["thermodynamics", "gibbs free energy", "spontaneity"],
                "estimated_time_seconds": 120,
            },
            {
                "id": uuid.uuid4(),
                "question_type": "standalone",
                "mcat_section": "CPBS",
                "topic_id": topic_objects[2].id,
                "foundational_concept_id": concept_objects[3].id,
                "difficulty_level": 2,
                "question_text": "A buffer solution contains equal concentrations of acetic acid (pKa = 4.76) and sodium acetate. What is the pH of this buffer?",
                "options": {
                    "A": "3.76",
                    "B": "4.76",
                    "C": "5.76",
                    "D": "7.00",
                },
                "correct_answer": "B",
                "correct_explanation": "Using the Henderson-Hasselbalch equation: pH = pKa + log([A-]/[HA]). When [A-] = [HA], the ratio is 1, and log(1) = 0. Therefore, pH = pKa = 4.76.",
                "incorrect_explanations": {
                    "A": "This would require more acid than conjugate base.",
                    "C": "This would require more conjugate base than acid.",
                    "D": "This is neutral pH, not related to the buffer's pKa.",
                },
                "tags": ["buffers", "henderson-hasselbalch", "pH"],
                "estimated_time_seconds": 90,
            },
            {
                "id": uuid.uuid4(),
                "question_type": "standalone",
                "mcat_section": "CPBS",
                "topic_id": topic_objects[3].id,
                "foundational_concept_id": concept_objects[4].id,
                "difficulty_level": 2,
                "question_text": "Which type of bond is formed by the sharing of electrons between two atoms?",
                "options": {
                    "A": "Ionic bond",
                    "B": "Covalent bond",
                    "C": "Hydrogen bond",
                    "D": "Van der Waals interaction",
                },
                "correct_answer": "B",
                "correct_explanation": "Covalent bonds are formed when two atoms share one or more pairs of electrons. This is distinct from ionic bonding (electron transfer) or intermolecular forces like hydrogen bonds.",
                "incorrect_explanations": {
                    "A": "Ionic bonds involve electron transfer, not sharing.",
                    "C": "Hydrogen bonds are intermolecular forces, not true chemical bonds.",
                    "D": "Van der Waals forces are weak intermolecular interactions.",
                },
                "tags": ["bonding", "covalent", "chemistry fundamentals"],
                "estimated_time_seconds": 60,
            },
            {
                "id": uuid.uuid4(),
                "question_type": "standalone",
                "mcat_section": "BBLS",
                "topic_id": topic_objects[4].id,
                "foundational_concept_id": concept_objects[6].id,
                "difficulty_level": 2,
                "question_text": "Which organelle is primarily responsible for protein synthesis in eukaryotic cells?",
                "options": {
                    "A": "Mitochondria",
                    "B": "Golgi apparatus",
                    "C": "Ribosome",
                    "D": "Lysosome",
                },
                "correct_answer": "C",
                "correct_explanation": "Ribosomes are the cellular organelles responsible for protein synthesis through translation of mRNA. They can be free in the cytoplasm or bound to the endoplasmic reticulum.",
                "incorrect_explanations": {
                    "A": "Mitochondria produce ATP through cellular respiration.",
                    "B": "The Golgi apparatus modifies and packages proteins, but doesn't synthesize them.",
                    "D": "Lysosomes contain digestive enzymes and break down cellular waste.",
                },
                "tags": ["cell biology", "ribosomes", "protein synthesis"],
                "estimated_time_seconds": 75,
            },
        ]

        for question_data in questions:
            question = Question(**question_data)
            db.add(question)
        db.commit()
        print(f"✅ Created {len(questions)} sample questions")

        print("\n🎉 Database seeding completed successfully!")
        print("\n📝 Demo User Credentials:")
        print("   Email: demo@mcatprep.com")
        print("   Password: demo123")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("MCAT Prep - Database Seeding Script")
    print("=" * 50)
    seed_database()
