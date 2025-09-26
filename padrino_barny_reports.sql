-- ¡¡¡ IMPORTANTE, PRIMERO CREAR LA BD Y LUEGO HACER LAS MIGRACIONES !!! -
CREATE DATABASE IF NOT EXISTS padrino_barny_reports;
USE padrino_barny_reports;

-- ¡¡¡ LUEGO DE HACER LAS MIGRACIONES PROCEDER A INSERTAR SÓLO SI YA SE CREÓ UN SUPERUSUARIO !!! --
INSERT INTO `auth_group` (`name`) VALUES ('Docentes');
INSERT INTO `auth_group_permissions` (`group_id`, `permission_id`)
SELECT (SELECT id FROM auth_group WHERE name = 'Docentes'), p.id FROM auth_permission p JOIN django_content_type ct ON p.content_type_id = ct.id WHERE
(ct.app_label = 'attention' AND ct.model = 'attention' AND p.codename IN ('add_attention', 'change_attention', 'delete_attention', 'view_attention')) OR
(ct.app_label = 'auth' AND ct.model = 'user' AND p.codename = 'view_user') OR
(ct.app_label = 'student' AND ct.model = 'student' AND p.codename = 'view_student') OR
(ct.app_label = 'subject' AND ct.model = 'subject' AND p.codename = 'view_subject');

INSERT INTO `auth_user` (`password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
('pbkdf2_sha256$1000000$ibPw8NaE5KHCDMPGumfyBc$G9ie5RMrF5DET+SnWgcutUEQJTrKjEguKKSM49h3guM=', NULL, 0, 'lrivas', 'Luis', 'Rivas', 'lrivas@univo.edu', 1, 1, CURRENT_TIMESTAMP),
('pbkdf2_sha256$1000000$ibPw8NaE5KHCDMPGumfyBc$G9ie5RMrF5DET+SnWgcutUEQJTrKjEguKKSM49h3guM=', NULL, 0, 'jdoe', 'John', 'Doe', 'jdoe@univo.edu', 1, 1, CURRENT_TIMESTAMP);

INSERT INTO `auth_user_groups` (`user_id`, `group_id`) VALUES
(2, (SELECT id FROM auth_group WHERE name = 'Docentes')),
(3, (SELECT id FROM auth_group WHERE name = 'Docentes'));

INSERT INTO `career` (`name`, `active`, `created_by_id`, `created_at`, `modified_by_id`, `updated_at`) VALUES
('Ingeniería de Sistemas Computacionales', TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
('Licenciatura en Ciencias Económicas', TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
('Licenciatura en Diseño Gráfico', TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

INSERT INTO `subject` (`name`, `section`, `active`, `created_by_id`, `created_at`, `modified_by_id`, `updated_at`) VALUES
('Gestión de Empresas de Desarrollo de Software', 'A', TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
('Bases de Datos II', 'B', TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
('Contabilidad Financiera I', 'A', TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
('Teoría del Color', 'C', TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

INSERT INTO `area` (`name`, `coordinator_id`, `active`, `created_by_id`, `created_at`, `modified_by_id`, `updated_at`) VALUES
('Departamento de Computación', 2, TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
('Departamento de Ciencias Económicas', 2, TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

INSERT INTO `student` (`first_name`, `last_name`, `carnet`, `email`, `career_id`, `active`, `created_by_id`, `created_at`, `modified_by_id`, `updated_at`) VALUES
('Juan', 'Pérez', 'JP202501', 'juan.perez@email.com', 1, TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
('María', 'Gómez', 'MG202402', 'maria.gomez@email.com', 2, TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP),
('Carlos', 'López', 'CL202303', 'carlos.lopez@email.com', 1, TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP);

INSERT INTO `student_subject` (`student_id`, `subject_id`, `active`, `created_by_id`, `created_at`, `modified_by_id`, `updated_at`) VALUES
(1, 1, TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP), -- Juan Pérez en Gestión de Empresas
(1, 2, TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP), -- Juan Pérez en Bases de Datos II
(2, 3, TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP), -- María Gómez en Contabilidad
(3, 1, TRUE, 1, CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP); -- Carlos López en Gestión de Empresas

INSERT INTO `attention` (`teacher_id`, `student_id`, `subject_id`, `description`, `channel`, `attention_date`, `active`, `created_by_id`, `created_at`, `modified_by_id`, `updated_at`) VALUES
(2, 1, 1, 'El estudiante consulta sobre la planificación de la transformación digital para la práctica 6.', 'IN_PERSON', '2025-09-22 10:30:00', TRUE, 2, CURRENT_TIMESTAMP, 2, CURRENT_TIMESTAMP),
(2, 3, 1, 'Se brinda apoyo vía WhatsApp sobre cómo estructurar el plan de trabajo de la etapa 1.', 'WHATSAPP', '2025-09-23 15:00:00', TRUE, 2, CURRENT_TIMESTAMP, 2, CURRENT_TIMESTAMP),
(3, 1, 2, 'Dudas sobre el uso de JOINs en SQL para la tarea de la semana.', 'EMAIL', '2025-09-24 09:00:00', TRUE, 3, CURRENT_TIMESTAMP, 3, CURRENT_TIMESTAMP),
(3, 2, 3, 'El estudiante solicitó una prórroga para la entrega del balance general. Se le explicó el procedimiento por correo.', 'EMAIL', '2025-09-25 11:45:00', TRUE, 3, CURRENT_TIMESTAMP, 3, CURRENT_TIMESTAMP);



