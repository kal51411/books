CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE legal_documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  source_type TEXT NOT NULL,
  title TEXT NOT NULL,
  act_name TEXT,
  section TEXT,
  subsection TEXT,
  court TEXT,
  judges TEXT[] DEFAULT '{}',
  citation TEXT,
  year INTEGER,
  state TEXT,
  jurisdiction TEXT NOT NULL DEFAULT 'unknown',
  source_url TEXT,
  enactment_date DATE,
  amendment_date DATE,
  effective_date DATE,
  repeal_status TEXT,
  version INTEGER NOT NULL DEFAULT 1,
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE legal_chunks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id UUID NOT NULL REFERENCES legal_documents(id) ON DELETE CASCADE,
  parent_id UUID REFERENCES legal_chunks(id),
  chunk_index INTEGER NOT NULL,
  section TEXT,
  paragraph INTEGER,
  text TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(document_id, chunk_index)
);

CREATE TABLE legal_versions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id UUID NOT NULL REFERENCES legal_documents(id) ON DELETE CASCADE,
  supersedes_id UUID REFERENCES legal_versions(id),
  enactment_date DATE,
  amendment_date DATE,
  effective_date DATE NOT NULL,
  repeal_status TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  roles TEXT[] NOT NULL DEFAULT '{researcher}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE chats (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  chat_id UUID NOT NULL REFERENCES chats(id) ON DELETE CASCADE,
  role TEXT NOT NULL,
  content TEXT NOT NULL,
  confidence NUMERIC(5,4),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE citations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  document_id UUID NOT NULL REFERENCES legal_documents(id),
  chunk_id UUID NOT NULL REFERENCES legal_chunks(id),
  paragraph INTEGER,
  label TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE retrieval_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  query TEXT NOT NULL,
  retrieved_chunk_ids UUID[] NOT NULL,
  scores JSONB NOT NULL DEFAULT '{}',
  latency_ms INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  principal TEXT NOT NULL,
  action TEXT NOT NULL,
  resource TEXT NOT NULL,
  ip_address INET,
  previous_hash TEXT,
  event_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
