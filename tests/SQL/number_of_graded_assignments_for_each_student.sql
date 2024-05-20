SELECT student_id, COUNT(*) as graded_count
FROM assignments
WHERE state = 'GRADED' AND grade = 'A'
GROUP BY student_id
ORDER BY graded_count DESC

-- Write query to get number of graded assignments for each student: --
