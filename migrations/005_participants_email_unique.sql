UPDATE participants SET email = lower(trim(email));
CREATE UNIQUE INDEX participants_email_unique ON participants (lower(trim(email)));
