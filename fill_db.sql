
INSERT INTO api_v1_handbook (id, uniq_code, title, description) VALUES
(1, '1', 'Специальности медицинских работников', 'Описание справочника 1'),
(2, '2', 'Специальности медицинских работников 2', 'Описание справочника 2');


INSERT INTO api_v1_versionhandbook (id, version, version_start_date, handbook_id) VALUES
(1, '1.0', '2024-01-01', 1),
(2, '2.0', '2024-06-01', 1);


INSERT INTO api_v1_handbookelement (id, version_hand_book_id, uniq_code, value) VALUES
(1, 1, '1', 'Врач-терапевт'),
(2, 1, '2', 'Травматолог-ортопед'),
(3, 1, '3', 'Хирург'),
(4, 2, '4', 'Лор');
