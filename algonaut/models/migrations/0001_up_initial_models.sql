
CREATE TABLE algonaut_version (
    version INTEGER
);

INSERT INTO algonaut_version (version) VALUES (1);

SET statement_timeout = 0;
SET client_encoding = 'UTF8';

-- Stores data about external organizations (e.g. their name) so we don't need
-- to fetch this data every time we want to access organization details

CREATE TABLE organization (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    source_id BYTEA NOT NULL,
    source CHARACTER VARYING NOT NULL,
    name CHARACTER VARYING NOT NULL,
    description CHARACTER VARYING NOT NULL DEFAULT '',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITHOUT TIME ZONE,
    data json
);

ALTER TABLE ONLY organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (id);

CREATE SEQUENCE organization_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE organization_id_seq OWNED BY organization.id;

ALTER TABLE ONLY organization ALTER COLUMN id SET DEFAULT nextval('organization_id_seq'::regclass);

ALTER TABLE ONLY organization
    ADD CONSTRAINT organization_ext_id_key UNIQUE (ext_id);

CREATE UNIQUE INDEX ix_organization_unique ON organization (source, source_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_organization_created_at ON organization USING BTREE (created_at);
CREATE INDEX ix_organization_updated_at ON organization USING BTREE (updated_at);
CREATE INDEX ix_organization_deleted_at ON organization USING BTREE (deleted_at);

-- represents a project
CREATE TABLE project (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    organization_id bigint NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    path CHARACTER VARYING NOT NULL,
    name CHARACTER VARYING NOT NULL,
    description CHARACTER VARYING NOT NULL DEFAULT '',
    tags CHARACTER VARYING[],
    data json
);

ALTER TABLE ONLY project
    ADD CONSTRAINT project_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY project
    ADD CONSTRAINT project_pkey PRIMARY KEY (id);

CREATE SEQUENCE project_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE project_id_seq OWNED BY project.id;

ALTER TABLE ONLY project ALTER COLUMN id SET DEFAULT nextval('project_id_seq'::regclass);

ALTER TABLE ONLY project
    ADD CONSTRAINT project_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES organization(id);

CREATE UNIQUE INDEX ix_project_organization_path ON project USING BTREE (organization_id, path) WHERE (deleted_at IS NULL);
CREATE INDEX ix_project_organization_id ON project USING BTREE (organization_id);
CREATE INDEX ix_project_tags ON project USING GIN (tags);
CREATE INDEX ix_project_path ON project USING BTREE (path);
CREATE INDEX ix_project_name ON project USING BTREE (name);
CREATE INDEX ix_project_created_at ON project USING BTREE (created_at);
CREATE INDEX ix_project_updated_at ON project USING BTREE (updated_at);
CREATE INDEX ix_project_deleted_at ON project USING BTREE (deleted_at);

-- represents a datapoint
CREATE TABLE datapoint (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    hash BYTEA NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json
);

ALTER TABLE ONLY datapoint
    ADD CONSTRAINT datapoint_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY datapoint
    ADD CONSTRAINT datapoint_pkey PRIMARY KEY (id);

CREATE SEQUENCE datapoint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE datapoint_id_seq OWNED BY datapoint.id;

ALTER TABLE ONLY datapoint ALTER COLUMN id SET DEFAULT nextval('datapoint_id_seq'::regclass);
CREATE UNIQUE INDEX ix_datapoint_unique_hash ON datapoint USING BTREE (hash) WHERE (deleted_at IS NULL);
CREATE INDEX ix_datapoint_created_at ON datapoint USING BTREE (created_at);
CREATE INDEX ix_datapoint_updated_at ON datapoint USING BTREE (updated_at);
CREATE INDEX ix_datapoint_deleted_at ON datapoint USING BTREE (deleted_at);

-- represents a dataset
CREATE TABLE dataset (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    hash BYTEA NOT NULL,
    name CHARACTER VARYING NOT NULL DEFAULT '',
    project_id bigint NOT NULL,
    tags CHARACTER VARYING[],
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json
);

ALTER TABLE ONLY dataset
    ADD CONSTRAINT dataset_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY dataset
    ADD CONSTRAINT dataset_pkey PRIMARY KEY (id);

CREATE SEQUENCE dataset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE dataset_id_seq OWNED BY dataset.id;

ALTER TABLE ONLY dataset ALTER COLUMN id SET DEFAULT nextval('dataset_id_seq'::regclass);

ALTER TABLE ONLY dataset
    ADD CONSTRAINT dataset_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(id);

CREATE UNIQUE INDEX ix_dataset_unique_hash ON dataset USING BTREE (hash, project_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_dataset_tags ON dataset USING GIN (tags);
CREATE INDEX ix_dataset_name ON dataset USING BTREE (name);
CREATE INDEX ix_dataset_created_at ON dataset USING BTREE (created_at);
CREATE INDEX ix_dataset_updated_at ON dataset USING BTREE (updated_at);
CREATE INDEX ix_dataset_deleted_at ON dataset USING BTREE (deleted_at);

-- represents a data schema
CREATE TABLE dataschema (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    hash BYTEA NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json
);

ALTER TABLE ONLY dataschema
    ADD CONSTRAINT dataschema_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY dataschema
    ADD CONSTRAINT dataschema_pkey PRIMARY KEY (id);

CREATE SEQUENCE dataschema_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE dataschema_id_seq OWNED BY dataschema.id;

ALTER TABLE ONLY dataschema ALTER COLUMN id SET DEFAULT nextval('dataschema_id_seq'::regclass);

CREATE UNIQUE INDEX ix_dataschema_unique_hash ON dataschema USING BTREE (hash) WHERE (deleted_at IS NULL);
CREATE INDEX ix_dataschema_created_at ON dataschema USING BTREE (created_at);
CREATE INDEX ix_dataschema_updated_at ON dataschema USING BTREE (updated_at);
CREATE INDEX ix_dataschema_deleted_at ON dataschema USING BTREE (deleted_at);

-- represents an algorithm
CREATE TABLE algorithm (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    tags CHARACTER VARYING[],
    hash BYTEA NOT NULL,
    name CHARACTER VARYING NOT NULL DEFAULT '',
    project_id bigint NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json
);

ALTER TABLE ONLY algorithm
    ADD CONSTRAINT algorithm_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY algorithm
    ADD CONSTRAINT algorithm_pkey PRIMARY KEY (id);

ALTER TABLE ONLY algorithm
    ADD CONSTRAINT algorithm_project_id_fkey FOREIGN KEY (project_id) REFERENCES project(id);

CREATE SEQUENCE algorithm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE algorithm_id_seq OWNED BY algorithm.id;

ALTER TABLE ONLY algorithm ALTER COLUMN id SET DEFAULT nextval('algorithm_id_seq'::regclass);

CREATE UNIQUE INDEX ix_algorithm_unique_hash ON algorithm USING BTREE (hash, project_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_algorithm_created_at ON algorithm USING BTREE (created_at);
CREATE INDEX ix_algorithm_updated_at ON algorithm USING BTREE (updated_at);
CREATE INDEX ix_algorithm_deleted_at ON algorithm USING BTREE (deleted_at);
CREATE INDEX ix_algorithm_tags ON algorithm USING GIN (tags);
CREATE INDEX ix_algorithm_name ON algorithm USING BTREE (name);

-- represents a model
CREATE TABLE model (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    hash BYTEA NOT NULL,
    algorithm_id bigint NOT NULL,
    dataset_id bigint NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json
);

ALTER TABLE ONLY model
    ADD CONSTRAINT model_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY model
    ADD CONSTRAINT model_pkey PRIMARY KEY (id);

CREATE SEQUENCE model_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE model_id_seq OWNED BY model.id;

ALTER TABLE ONLY model ALTER COLUMN id SET DEFAULT nextval('model_id_seq'::regclass);

CREATE UNIQUE INDEX ix_model_unique_hash ON model USING BTREE (algorithm_id, dataset_id, hash) WHERE (deleted_at IS NULL);
CREATE INDEX ix_model_hash ON model USING BTREE (hash);
CREATE INDEX ix_model_created_at ON model USING BTREE (created_at);
CREATE INDEX ix_model_updated_at ON model USING BTREE (updated_at);
CREATE INDEX ix_model_deleted_at ON model USING BTREE (deleted_at);

ALTER TABLE ONLY model
    ADD CONSTRAINT model_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset(id);

ALTER TABLE ONLY model
    ADD CONSTRAINT model_algorithm_id_fkey FOREIGN KEY (algorithm_id) REFERENCES algorithm(id);

-- represents an algorithm schema
CREATE TABLE algorithmschema (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    hash BYTEA NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    -- contains the actual algorithm schema
    data json
);

ALTER TABLE ONLY algorithmschema
    ADD CONSTRAINT algorithmschema_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY algorithmschema
    ADD CONSTRAINT algorithmschema_pkey PRIMARY KEY (id);

CREATE SEQUENCE algorithmschema_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE algorithmschema_id_seq OWNED BY algorithmschema.id;

ALTER TABLE ONLY algorithmschema ALTER COLUMN id SET DEFAULT nextval('algorithmschema_id_seq'::regclass);

CREATE UNIQUE INDEX ix_algorithmschema_unique_hash ON algorithmschema USING BTREE (hash) WHERE (deleted_at IS NULL);
CREATE INDEX ix_algorithmschema_created_at ON algorithmschema USING BTREE (created_at);
CREATE INDEX ix_algorithmschema_updated_at ON algorithmschema USING BTREE (updated_at);
CREATE INDEX ix_algorithmschema_deleted_at ON algorithmschema USING BTREE (deleted_at);

-- represents a test result
CREATE TABLE result (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    name CHARACTER VARYING NOT NULL,
    version CHARACTER VARYING NOT NULL,
    hash BYTEA NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    -- contains the actual result data (can be deeply nested)
    data json
);

ALTER TABLE ONLY result
    ADD CONSTRAINT result_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY result
    ADD CONSTRAINT result_pkey PRIMARY KEY (id);

CREATE SEQUENCE result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE result_id_seq OWNED BY result.id;

ALTER TABLE ONLY result ALTER COLUMN id SET DEFAULT nextval('result_id_seq'::regclass);

CREATE UNIQUE INDEX ix_result_unique_hash ON result USING BTREE (hash) WHERE (deleted_at IS NULL);
CREATE INDEX ix_result_name ON result USING BTREE (name);
CREATE INDEX ix_result_version ON result USING BTREE (version);
CREATE INDEX ix_result_created_at ON result USING BTREE (created_at);
CREATE INDEX ix_result_updated_at ON result USING BTREE (updated_at);
CREATE INDEX ix_result_deleted_at ON result USING BTREE (deleted_at);

/*
Association tables
*/

-- maps a result to a given algorithn version
CREATE TABLE algorithm_result (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    algorithm_id bigint NOT NULL,
    result_id bigint NOT NULL
);

ALTER TABLE ONLY algorithm_result
    ADD CONSTRAINT algorithm_result_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY algorithm_result
    ADD CONSTRAINT algorithm_result_pkey PRIMARY KEY (id);

CREATE SEQUENCE algorithm_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE algorithm_result_id_seq OWNED BY algorithm_result.id;

ALTER TABLE ONLY algorithm_result ALTER COLUMN id SET DEFAULT nextval('algorithm_result_id_seq'::regclass);

ALTER TABLE ONLY algorithm_result
    ADD CONSTRAINT algorithm_result_algorithm_id_fkey FOREIGN KEY (algorithm_id) REFERENCES algorithm(id);

ALTER TABLE ONLY algorithm_result
    ADD CONSTRAINT algorithm_result_result_id_fkey FOREIGN KEY (result_id) REFERENCES result(id);

-- an algorithm version can only be mapped to a result once
CREATE UNIQUE INDEX ix_algorithm_result_unique ON algorithm_result USING BTREE (algorithm_id, result_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_algorithm_result_created_at ON algorithm_result USING BTREE (created_at);
CREATE INDEX ix_algorithm_result_updated_at ON algorithm_result USING BTREE (updated_at);
CREATE INDEX ix_algorithm_result_deleted_at ON algorithm_result USING BTREE (deleted_at);

-- maps a result to a given dataset version
CREATE TABLE dataset_result (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    dataset_id bigint NOT NULL,
    result_id bigint NOT NULL
);

ALTER TABLE ONLY dataset_result
    ADD CONSTRAINT dataset_result_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY dataset_result
    ADD CONSTRAINT dataset_result_pkey PRIMARY KEY (id);

CREATE SEQUENCE dataset_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE dataset_result_id_seq OWNED BY dataset_result.id;

ALTER TABLE ONLY dataset_result ALTER COLUMN id SET DEFAULT nextval('dataset_result_id_seq'::regclass);

ALTER TABLE ONLY dataset_result
    ADD CONSTRAINT dataset_result_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset(id);

ALTER TABLE ONLY dataset_result
    ADD CONSTRAINT dataset_result_result_id_fkey FOREIGN KEY (result_id) REFERENCES result(id);

-- a dataset version can only be mapped to a result once
CREATE UNIQUE INDEX ix_dataset_result_unique ON dataset_result USING BTREE (dataset_id, result_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_dataset_result_created_at ON dataset_result USING BTREE (created_at);
CREATE INDEX ix_dataset_result_updated_at ON dataset_result USING BTREE (updated_at);
CREATE INDEX ix_dataset_result_deleted_at ON dataset_result USING BTREE (deleted_at);

-- maps a result to a given model
CREATE TABLE model_result (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    model_id bigint NOT NULL,
    result_id bigint NOT NULL
);

ALTER TABLE ONLY model_result
    ADD CONSTRAINT model_result_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY model_result
    ADD CONSTRAINT model_result_pkey PRIMARY KEY (id);

CREATE SEQUENCE model_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE model_result_id_seq OWNED BY model_result.id;

ALTER TABLE ONLY model_result ALTER COLUMN id SET DEFAULT nextval('model_result_id_seq'::regclass);

ALTER TABLE ONLY model_result
    ADD CONSTRAINT model_result_model_id_fkey FOREIGN KEY (model_id) REFERENCES model(id);

ALTER TABLE ONLY model_result
    ADD CONSTRAINT model_result_result_id_fkey FOREIGN KEY (result_id) REFERENCES result(id);

-- a result can only be mapped to a model once
CREATE UNIQUE INDEX ix_model_result_unique ON model_result USING BTREE (model_id, result_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_model_result_created_at ON model_result USING BTREE (created_at);
CREATE INDEX ix_model_result_updated_at ON model_result USING BTREE (updated_at);
CREATE INDEX ix_model_result_deleted_at ON model_result USING BTREE (deleted_at);

-- maps a result to a given datapoint and model
CREATE TABLE datapoint_model_result (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    datapoint_id bigint NOT NULL,
    model_id bigint NOT NULL,
    result_id bigint NOT NULL
);

ALTER TABLE ONLY datapoint_model_result
    ADD CONSTRAINT datapoint_model_result_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY datapoint_model_result
    ADD CONSTRAINT datapoint_model_result_pkey PRIMARY KEY (id);

CREATE SEQUENCE datapoint_model_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE datapoint_model_result_id_seq OWNED BY datapoint_model_result.id;

ALTER TABLE ONLY datapoint_model_result ALTER COLUMN id SET DEFAULT nextval('datapoint_model_result_id_seq'::regclass);

ALTER TABLE ONLY datapoint_model_result
    ADD CONSTRAINT datapoint_model_result_model_id_fkey FOREIGN KEY (model_id) REFERENCES model(id);

ALTER TABLE ONLY datapoint_model_result
    ADD CONSTRAINT datapoint_model_result_datapoint_id_fkey FOREIGN KEY (datapoint_id) REFERENCES datapoint(id);

ALTER TABLE ONLY datapoint_model_result
    ADD CONSTRAINT datapoint_model_result_result_id_fkey FOREIGN KEY (result_id) REFERENCES result(id);

-- a result can only be mapped to a model once
CREATE UNIQUE INDEX ix_datapoint_model_result_unique ON datapoint_model_result USING BTREE (datapoint_id, model_id, result_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_datapoint_model_result_created_at ON datapoint_model_result USING BTREE (created_at);
CREATE INDEX ix_datapoint_model_result_updated_at ON datapoint_model_result USING BTREE (updated_at);
CREATE INDEX ix_datapoint_model_result_deleted_at ON datapoint_model_result USING BTREE (deleted_at);


-- maps a result to a given dataset and model
CREATE TABLE dataset_model_result (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    dataset_id bigint NOT NULL,
    model_id bigint NOT NULL,
    result_id bigint NOT NULL
);

ALTER TABLE ONLY dataset_model_result
    ADD CONSTRAINT dataset_model_result_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY dataset_model_result
    ADD CONSTRAINT dataset_model_result_pkey PRIMARY KEY (id);

CREATE SEQUENCE dataset_model_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE dataset_model_result_id_seq OWNED BY dataset_model_result.id;

ALTER TABLE ONLY dataset_model_result ALTER COLUMN id SET DEFAULT nextval('dataset_model_result_id_seq'::regclass);

ALTER TABLE ONLY dataset_model_result
    ADD CONSTRAINT dataset_model_result_model_id_fkey FOREIGN KEY (model_id) REFERENCES model(id);

ALTER TABLE ONLY dataset_model_result
    ADD CONSTRAINT dataset_model_result_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset(id);

ALTER TABLE ONLY dataset_model_result
    ADD CONSTRAINT dataset_model_result_result_id_fkey FOREIGN KEY (result_id) REFERENCES result(id);

-- a result can only be mapped to a model once
CREATE UNIQUE INDEX ix_dataset_model_result_unique ON dataset_model_result USING BTREE (dataset_id, model_id, result_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_dataset_model_result_created_at ON dataset_model_result USING BTREE (created_at);
CREATE INDEX ix_dataset_model_result_updated_at ON dataset_model_result USING BTREE (updated_at);
CREATE INDEX ix_dataset_model_result_deleted_at ON dataset_model_result USING BTREE (deleted_at);

-- maps a dataset version to a data schema
CREATE TABLE dataset_dataschema (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    dataset_id bigint NOT NULL,
    dataschema_id bigint NOT NULL
);

ALTER TABLE ONLY dataset_dataschema
    ADD CONSTRAINT dataset_dataschema_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY dataset_dataschema
    ADD CONSTRAINT dataset_dataschema_pkey PRIMARY KEY (id);

CREATE SEQUENCE dataset_dataschema_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE dataset_dataschema_id_seq OWNED BY dataset_dataschema.id;

ALTER TABLE ONLY dataset_dataschema ALTER COLUMN id SET DEFAULT nextval('dataset_dataschema_id_seq'::regclass);

ALTER TABLE ONLY dataset_dataschema
    ADD CONSTRAINT dataset_dataschema_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset(id);

ALTER TABLE ONLY dataset_dataschema
    ADD CONSTRAINT dataset_dataschema_dataschema_id_fkey FOREIGN KEY (dataschema_id) REFERENCES dataschema(id);

-- a dataset schema can only be mapped to a dataset version once
CREATE UNIQUE INDEX ix_dataset_dataschema_unique ON dataset_dataschema USING BTREE (dataset_id, dataschema_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_dataset_dataschema_created_at ON dataset_dataschema USING BTREE (created_at);
CREATE INDEX ix_dataset_dataschema_updated_at ON dataset_dataschema USING BTREE (updated_at);
CREATE INDEX ix_dataset_dataschema_deleted_at ON dataset_dataschema USING BTREE (deleted_at);

-- maps an algorithm schema to an algorithm version
CREATE TABLE algorithm_algorithmschema (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    algorithm_id bigint NOT NULL,
    algorithmschema_id bigint NOT NULL
);

ALTER TABLE ONLY algorithm_algorithmschema
    ADD CONSTRAINT algorithm_algorithmschema_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY algorithm_algorithmschema
    ADD CONSTRAINT algorithm_algorithmschema_pkey PRIMARY KEY (id);

CREATE SEQUENCE algorithm_algorithmschema_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE algorithm_algorithmschema_id_seq OWNED BY algorithm_algorithmschema.id;

ALTER TABLE ONLY algorithm_algorithmschema ALTER COLUMN id SET DEFAULT nextval('algorithm_algorithmschema_id_seq'::regclass);

ALTER TABLE ONLY algorithm_algorithmschema
    ADD CONSTRAINT algorithm_algorithmschema_algorithm_id_fkey FOREIGN KEY (algorithm_id) REFERENCES algorithm(id);

ALTER TABLE ONLY algorithm_algorithmschema
    ADD CONSTRAINT algorithm_algorithmschema_algorithmschema_id_fkey FOREIGN KEY (algorithmschema_id) REFERENCES algorithmschema(id);

-- an algorithm schema can only be mapped to an algorithm version once
CREATE UNIQUE INDEX ix_algorithm_algorithmschema_unique ON algorithm_algorithmschema USING BTREE (algorithm_id, algorithmschema_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_algorithm_algorithmschema_created_at ON algorithm_algorithmschema USING BTREE (created_at);
CREATE INDEX ix_algorithm_algorithmschema_updated_at ON algorithm_algorithmschema USING BTREE (updated_at);
CREATE INDEX ix_algorithm_algorithmschema_deleted_at ON algorithm_algorithmschema USING BTREE (deleted_at);

-- maps a datapoint to a given dataset version
CREATE TABLE dataset_datapoint (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    dataset_id bigint NOT NULL,
    datapoint_id bigint NOT NULL
);

ALTER TABLE ONLY dataset_datapoint
    ADD CONSTRAINT dataset_datapoint_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY dataset_datapoint
    ADD CONSTRAINT dataset_datapoint_pkey PRIMARY KEY (id);

CREATE SEQUENCE dataset_datapoint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE dataset_datapoint_id_seq OWNED BY dataset_datapoint.id;

ALTER TABLE ONLY dataset_datapoint ALTER COLUMN id SET DEFAULT nextval('dataset_datapoint_id_seq'::regclass);

ALTER TABLE ONLY dataset_datapoint
    ADD CONSTRAINT dataset_datapoint_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset(id);

ALTER TABLE ONLY dataset_datapoint
    ADD CONSTRAINT dataset_datapoint_datapoint_id_fkey FOREIGN KEY (datapoint_id) REFERENCES datapoint(id);

-- a datapoint can only be mapped to a dataset version once
CREATE UNIQUE INDEX ix_dataset_datapoint_unique ON dataset_datapoint USING BTREE (dataset_id, datapoint_id) WHERE (deleted_at IS NULL);
CREATE INDEX ix_dataset_datapoint_created_at ON dataset_datapoint USING BTREE (created_at);
CREATE INDEX ix_dataset_datapoint_updated_at ON dataset_datapoint USING BTREE (updated_at);
CREATE INDEX ix_dataset_datapoint_deleted_at ON dataset_datapoint USING BTREE (deleted_at);

-- models for role-based access concept

CREATE TYPE obj_role AS ENUM ('superuser', 'admin', 'developer', 'viewer', 'auditor');

-- object roles for organizations
CREATE TABLE object_role (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    object_id bigint NOT NULL,
    organization_id bigint NOT NULL,
    organization_role CHARACTER VARYING NOT NULL, --the role in the organization
    object_type CHARACTER VARYING NOT NULL,
    object_role obj_role NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITHOUT TIME ZONE
);

ALTER TABLE ONLY object_role
    ADD CONSTRAINT object_role_pkey PRIMARY KEY (id);

ALTER TABLE ONLY object_role
    ADD CONSTRAINT object_role_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES organization(id);

CREATE SEQUENCE object_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE object_role_id_seq OWNED BY object_role.id;

ALTER TABLE ONLY object_role ALTER COLUMN id SET DEFAULT nextval('object_role_id_seq'::regclass);

ALTER TABLE ONLY object_role
    ADD CONSTRAINT object_role_ext_id_key UNIQUE (ext_id);

CREATE UNIQUE INDEX ix_object_role_unique ON object_role (object_type, object_id, organization_id, organization_role, object_role) WHERE (deleted_at IS NULL);
CREATE INDEX ix_object_role_created_at ON object_role USING BTREE (created_at);
CREATE INDEX ix_object_role_updated_at ON object_role USING BTREE (updated_at);
CREATE INDEX ix_object_role_deleted_at ON object_role USING BTREE (deleted_at);

CREATE INDEX
    ix_object_role_object_role
ON
    object_role(
        object_id,
        organization_id,
        object_role,
        organization_role,
        object_type
    );
