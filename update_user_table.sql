
ALTER TABLE "user"
RENAME COLUMN user_type TO role;
-- set it from string to enum
ALTER TABLE "user"
ALTER COLUMN role
TYPE user_role_enum
USING role::user_role_enum;