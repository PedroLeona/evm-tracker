-- Optional demo data: one project with three activities in different situations.
-- Hand-computed consolidated result:
--   BAC 80000 | PV 52000 | EV 42500 | AC 50000
--   CPI 0.8500 | SPI 0.8173 | EAC 94117.65 | VAC -14117.65

INSERT INTO projects (name, description)
VALUES ('ERP migration', 'Demo project for the Earned Value dashboard');

INSERT INTO activities (project_id, name, budget_at_completion, planned_percent, actual_percent, actual_cost)
VALUES
    (1, 'Design',      20000, 100, 100, 18000),
    (1, 'Development', 50000,  60,  40, 30000),
    (1, 'Testing',     10000,  20,  25,  2000);
