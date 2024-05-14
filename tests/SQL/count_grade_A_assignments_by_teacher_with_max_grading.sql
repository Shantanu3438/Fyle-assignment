-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT COUNT(*) AS grade_A_count  
FROM assignments AS a
JOIN teachers AS t ON a.teacher_id = t.id 
WHERE a.grade = 'A'  
GROUP BY t.id  
ORDER BY grade_A_count DESC
LIMIT 1; 