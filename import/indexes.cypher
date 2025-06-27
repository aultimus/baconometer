// Create indexes for efficient lookups
CREATE INDEX actor_lowercase_name_index IF NOT EXISTS FOR (a:Actor) ON (a.lowercase_name);
