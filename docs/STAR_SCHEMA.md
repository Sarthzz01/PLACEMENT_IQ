# Star Schema

Fact table: `FactPlacement`

Dimensions:
- `DimStudent`: age, gender, branch
- `DimAcademic`: CGPA, backlogs, attendance
- `DimSkills`: coding/DSA/LeetCode/HackerRank/aptitude/communication/certifications
- `DimEngagement`: internships, projects, hackathons, GitHub, mock interview, training
- `DimPlacement`: placement target and status

The fact table stores measurable placement-related values and links to dimensions through `student_key`.
