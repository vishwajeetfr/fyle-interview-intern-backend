-- Write query to find the number of grade A's given by the teacher who has graded the most assignments

-- tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql
WITH teacher_assignment_counts AS (
    SELECT 
        teacher_id,
        COUNT(*) AS total_assignments
    FROM 
        assignments
    WHERE 
        teacher_id IS NOT NULL AND 
        grade IS NOT NULL
    GROUP BY 
        teacher_id
),
teacher_with_max_assignments AS (
    SELECT 
        teacher_id
    FROM 
        teacher_assignment_counts
    ORDER BY 
        total_assignments DESC
    LIMIT 1
)
SELECT 
    COUNT(*)
FROM 
    assignments
WHERE 
    teacher_id = (SELECT teacher_id FROM teacher_with_max_assignments)
    AND grade = 'A';
