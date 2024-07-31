SELECT student_id, COUNT(id) AS graded_assignments
FROM assignments
WHERE state = 'GRADED'
GROUP BY student_id;
