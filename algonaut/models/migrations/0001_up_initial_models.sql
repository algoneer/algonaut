
CREATE TABLE algonaut_version (
    version INTEGER
);

INSERT INTO algonaut_version (version) VALUES (1);

SET statement_timeout = 0;
SET client_encoding = 'UTF8';

/*
we need tables for dataset, datapoint, dataschema, algorithm, model,
algorithmschema and result.

We should be able to efficiently manage different versions of algorithms
as well as datasets, and to associate them with a given schema:

- algorithm_version -> (algorithm, algorithmschema)
- model -> (algorithm_version, dataset_version)
- datapoint -> datapoint_dataset_version -> dataset_version -> (dataset, dataschema)
- model a result for a given algorithm version
- result -> algorithm_version_result -> algorithm_version
- result -> dataset_version_result -> dataset_version

A given model always corresponds to a given algorithm version that was trained
with a given dataset version. There might be more than one model trained for
a given algorithm and dataset, e.g. trained with different hyper-parameters.

A given dataset version always belongs to a given dataset. A specific datapoint
always belongs to one or more datasets.
*/

-- represents a model
CREATE TABLE model (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    algorithmversion_id bigint NOT NULL,
    datasetversion_id bigint NOT NULL,
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

CREATE INDEX ix_model_created_at ON model USING BTREE (created_at);
CREATE INDEX ix_model_updated_at ON model USING BTREE (updated_at);
CREATE INDEX ix_model_deleted_at ON model USING BTREE (deleted_at);

-- represents a dataset
CREATE TABLE dataset (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    path CHARACTER VARYING NOT NULL,
    description CHARACTER VARYING NOT NULL DEFAULT '',
    tags CHARACTER VARYING[],
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

CREATE INDEX ix_dataset_tags ON dataset USING GIN (tags);
CREATE INDEX ix_dataset_path ON dataset USING BTREE (path);
CREATE INDEX ix_dataset_created_at ON dataset USING BTREE (created_at);
CREATE INDEX ix_dataset_updated_at ON dataset USING BTREE (updated_at);
CREATE INDEX ix_dataset_deleted_at ON dataset USING BTREE (deleted_at);

-- represents a datapoint
CREATE TABLE datapoint (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
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

CREATE INDEX ix_datapoint_created_at ON datapoint USING BTREE (created_at);
CREATE INDEX ix_datapoint_updated_at ON datapoint USING BTREE (updated_at);
CREATE INDEX ix_datapoint_deleted_at ON datapoint USING BTREE (deleted_at);

-- represents a dataset version
CREATE TABLE datasetversion (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    hash BYTEA NOT NULL,
    name CHARACTER VARYING NOT NULL DEFAULT '',
    dataset_id bigint NOT NULL,
    tags CHARACTER VARYING[],
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json
);

ALTER TABLE ONLY datasetversion
    ADD CONSTRAINT datasetversion_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY datasetversion
    ADD CONSTRAINT datasetversion_pkey PRIMARY KEY (id);

CREATE SEQUENCE datasetversion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE datasetversion_id_seq OWNED BY datasetversion.id;

ALTER TABLE ONLY datasetversion ALTER COLUMN id SET DEFAULT nextval('datasetversion_id_seq'::regclass);

ALTER TABLE ONLY model
    ADD CONSTRAINT model_datasetversion_id_fkey FOREIGN KEY (datasetversion_id) REFERENCES datasetversion(id);

ALTER TABLE ONLY datasetversion
    ADD CONSTRAINT datasetversion_dataset_id_fkey FOREIGN KEY (dataset_id) REFERENCES dataset(id);

CREATE UNIQUE INDEX ix_datasetversion_hash ON datasetversion USING BTREE (hash);
CREATE INDEX ix_datasetversion_tags ON datasetversion USING GIN (tags);
CREATE INDEX ix_datasetversion_name ON datasetversion USING BTREE (name);
CREATE INDEX ix_datasetversion_created_at ON datasetversion USING BTREE (created_at);
CREATE INDEX ix_datasetversion_updated_at ON datasetversion USING BTREE (updated_at);
CREATE INDEX ix_datasetversion_deleted_at ON datasetversion USING BTREE (deleted_at);

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

CREATE UNIQUE INDEX ix_dataschema_hash ON dataschema USING BTREE (hash);
CREATE INDEX ix_dataschema_created_at ON dataschema USING BTREE (created_at);
CREATE INDEX ix_dataschema_updated_at ON dataschema USING BTREE (updated_at);
CREATE INDEX ix_dataschema_deleted_at ON dataschema USING BTREE (deleted_at);

-- represents an algorithm
CREATE TABLE algorithm (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    path CHARACTER VARYING NOT NULL,
    description CHARACTER VARYING NOT NULL DEFAULT '',
    tags CHARACTER VARYING[],
    data json
);

ALTER TABLE ONLY algorithm
    ADD CONSTRAINT algorithm_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY algorithm
    ADD CONSTRAINT algorithm_pkey PRIMARY KEY (id);

CREATE SEQUENCE algorithm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE algorithm_id_seq OWNED BY algorithm.id;

ALTER TABLE ONLY algorithm ALTER COLUMN id SET DEFAULT nextval('algorithm_id_seq'::regclass);

CREATE INDEX ix_algorithm_tags ON algorithm USING GIN (tags);
CREATE INDEX ix_algorithm_path ON algorithm USING BTREE (path);
CREATE INDEX ix_algorithm_created_at ON algorithm USING BTREE (created_at);
CREATE INDEX ix_algorithm_updated_at ON algorithm USING BTREE (updated_at);
CREATE INDEX ix_algorithm_deleted_at ON algorithm USING BTREE (deleted_at);

-- represents an algorithm version
CREATE TABLE algorithmversion (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    tags CHARACTER VARYING[],
    hash BYTEA NOT NULL,
    name CHARACTER VARYING NOT NULL DEFAULT '',
    algorithm_id bigint NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json
);

ALTER TABLE ONLY algorithmversion
    ADD CONSTRAINT algorithmversion_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY algorithmversion
    ADD CONSTRAINT algorithmversion_pkey PRIMARY KEY (id);

ALTER TABLE ONLY algorithmversion
    ADD CONSTRAINT algorithmversion_algorithm_id_fkey FOREIGN KEY (algorithm_id) REFERENCES algorithm(id);

ALTER TABLE ONLY model
    ADD CONSTRAINT model_algorithmversion_id_fkey FOREIGN KEY (algorithmversion_id) REFERENCES algorithmversion(id);

CREATE SEQUENCE algorithmversion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE algorithmversion_id_seq OWNED BY algorithmversion.id;

ALTER TABLE ONLY algorithmversion ALTER COLUMN id SET DEFAULT nextval('algorithmversion_id_seq'::regclass);

CREATE UNIQUE INDEX ix_algorithmversion_hash ON algorithmversion USING BTREE (hash);
CREATE INDEX ix_algorithmversion_created_at ON algorithmversion USING BTREE (created_at);
CREATE INDEX ix_algorithmversion_updated_at ON algorithmversion USING BTREE (updated_at);
CREATE INDEX ix_algorithmversion_deleted_at ON algorithmversion USING BTREE (deleted_at);
CREATE INDEX ix_algorithmversion_tags ON algorithmversion USING GIN (tags);
CREATE INDEX ix_algorithmversion_name ON algorithmversion USING BTREE (name);

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

CREATE UNIQUE INDEX ix_algorithmschema_hash ON algorithmschema USING BTREE (hash);
CREATE INDEX ix_algorithmschema_created_at ON algorithmschema USING BTREE (created_at);
CREATE INDEX ix_algorithmschema_updated_at ON algorithmschema USING BTREE (updated_at);
CREATE INDEX ix_algorithmschema_deleted_at ON algorithmschema USING BTREE (deleted_at);

-- represents a test result
CREATE TABLE result (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
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

/*
Association tables
*/

-- maps a result to a given algorithn version
CREATE TABLE algorithmversion_result (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    algorithmversion_id bigint NOT NULL,
    result_id bigint NOT NULL
);

ALTER TABLE ONLY algorithmversion_result
    ADD CONSTRAINT algorithmversion_result_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY algorithmversion_result
    ADD CONSTRAINT algorithmversion_result_pkey PRIMARY KEY (id);

CREATE SEQUENCE algorithmversion_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE algorithmversion_result_id_seq OWNED BY algorithmversion_result.id;

ALTER TABLE ONLY algorithmversion_result ALTER COLUMN id SET DEFAULT nextval('algorithmversion_result_id_seq'::regclass);

ALTER TABLE ONLY algorithmversion_result
    ADD CONSTRAINT algorithmversion_result_algorithmversion_id_fkey FOREIGN KEY (algorithmversion_id) REFERENCES algorithmversion(id);

ALTER TABLE ONLY algorithmversion_result
    ADD CONSTRAINT algorithmversion_result_result_id_fkey FOREIGN KEY (result_id) REFERENCES result(id);

-- an algorithm version can only be mapped to a result once
CREATE UNIQUE INDEX ix_algorithmversion_result_unique ON algorithmversion_result USING BTREE (algorithmversion_id, result_id);
CREATE INDEX ix_algorithmversion_result_created_at ON algorithmversion_result USING BTREE (created_at);
CREATE INDEX ix_algorithmversion_result_updated_at ON algorithmversion_result USING BTREE (updated_at);
CREATE INDEX ix_algorithmversion_result_deleted_at ON algorithmversion_result USING BTREE (deleted_at);

-- maps a result to a given dataset version
CREATE TABLE datasetversion_result (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    datasetversion_id bigint NOT NULL,
    result_id bigint NOT NULL
);

ALTER TABLE ONLY datasetversion_result
    ADD CONSTRAINT datasetversion_result_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY datasetversion_result
    ADD CONSTRAINT datasetversion_result_pkey PRIMARY KEY (id);

CREATE SEQUENCE datasetversion_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE datasetversion_result_id_seq OWNED BY datasetversion_result.id;

ALTER TABLE ONLY datasetversion_result ALTER COLUMN id SET DEFAULT nextval('datasetversion_result_id_seq'::regclass);

ALTER TABLE ONLY datasetversion_result
    ADD CONSTRAINT datasetversion_result_datasetversion_id_fkey FOREIGN KEY (datasetversion_id) REFERENCES datasetversion(id);

ALTER TABLE ONLY datasetversion_result
    ADD CONSTRAINT datasetversion_result_result_id_fkey FOREIGN KEY (result_id) REFERENCES result(id);

-- a dataset version can only be mapped to a result once
CREATE UNIQUE INDEX ix_datasetversion_result_unique ON datasetversion_result USING BTREE (datasetversion_id, result_id);
CREATE INDEX ix_datasetversion_result_created_at ON datasetversion_result USING BTREE (created_at);
CREATE INDEX ix_datasetversion_result_updated_at ON datasetversion_result USING BTREE (updated_at);
CREATE INDEX ix_datasetversion_result_deleted_at ON datasetversion_result USING BTREE (deleted_at);

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
CREATE UNIQUE INDEX ix_model_result_unique ON model_result USING BTREE (model_id, result_id);
CREATE INDEX ix_model_result_created_at ON model_result USING BTREE (created_at);
CREATE INDEX ix_model_result_updated_at ON model_result USING BTREE (updated_at);
CREATE INDEX ix_model_result_deleted_at ON model_result USING BTREE (deleted_at);

-- maps a dataset version to a data schema
CREATE TABLE datasetversion_dataschema (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    datasetversion_id bigint NOT NULL,
    dataschema_id bigint NOT NULL
);

ALTER TABLE ONLY datasetversion_dataschema
    ADD CONSTRAINT datasetversion_dataschema_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY datasetversion_dataschema
    ADD CONSTRAINT datasetversion_dataschema_pkey PRIMARY KEY (id);

CREATE SEQUENCE datasetversion_dataschema_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE datasetversion_dataschema_id_seq OWNED BY datasetversion_dataschema.id;

ALTER TABLE ONLY datasetversion_dataschema ALTER COLUMN id SET DEFAULT nextval('datasetversion_dataschema_id_seq'::regclass);

ALTER TABLE ONLY datasetversion_dataschema
    ADD CONSTRAINT datasetversion_dataschema_datasetversion_id_fkey FOREIGN KEY (datasetversion_id) REFERENCES datasetversion(id);

ALTER TABLE ONLY datasetversion_dataschema
    ADD CONSTRAINT datasetversion_dataschema_dataschema_id_fkey FOREIGN KEY (dataschema_id) REFERENCES dataschema(id);

-- a dataset schema can only be mapped to a dataset version once
CREATE UNIQUE INDEX ix_datasetversion_dataschema_unique ON datasetversion_dataschema USING BTREE (datasetversion_id, dataschema_id);
CREATE INDEX ix_datasetversion_dataschema_created_at ON datasetversion_dataschema USING BTREE (created_at);
CREATE INDEX ix_datasetversion_dataschema_updated_at ON datasetversion_dataschema USING BTREE (updated_at);
CREATE INDEX ix_datasetversion_dataschema_deleted_at ON datasetversion_dataschema USING BTREE (deleted_at);

-- maps an algorithm schema to an algorithm version
CREATE TABLE algorithmversion_algorithmschema (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    algorithmversion_id bigint NOT NULL,
    algorithmschema_id bigint NOT NULL
);

ALTER TABLE ONLY algorithmversion_algorithmschema
    ADD CONSTRAINT algorithmversion_algorithmschema_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY algorithmversion_algorithmschema
    ADD CONSTRAINT algorithmversion_algorithmschema_pkey PRIMARY KEY (id);

CREATE SEQUENCE algorithmversion_algorithmschema_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE algorithmversion_algorithmschema_id_seq OWNED BY algorithmversion_algorithmschema.id;

ALTER TABLE ONLY algorithmversion_algorithmschema ALTER COLUMN id SET DEFAULT nextval('algorithmversion_algorithmschema_id_seq'::regclass);

ALTER TABLE ONLY algorithmversion_algorithmschema
    ADD CONSTRAINT algorithmversion_algorithmschema_algorithmversion_id_fkey FOREIGN KEY (algorithmversion_id) REFERENCES algorithmversion(id);

ALTER TABLE ONLY algorithmversion_algorithmschema
    ADD CONSTRAINT algorithmversion_algorithmschema_algorithmschema_id_fkey FOREIGN KEY (algorithmschema_id) REFERENCES algorithmschema(id);

-- an algorithm schema can only be mapped to an algorithm version once
CREATE UNIQUE INDEX ix_algorithmversion_algorithmschema_unique ON algorithmversion_algorithmschema USING BTREE (algorithmversion_id, algorithmschema_id);
CREATE INDEX ix_algorithmversion_algorithmschema_created_at ON algorithmversion_algorithmschema USING BTREE (created_at);
CREATE INDEX ix_algorithmversion_algorithmschema_updated_at ON algorithmversion_algorithmschema USING BTREE (updated_at);
CREATE INDEX ix_algorithmversion_algorithmschema_deleted_at ON algorithmversion_algorithmschema USING BTREE (deleted_at);

-- maps a datapoint to a given dataset version
CREATE TABLE datasetversion_datapoint (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    deleted_at timestamp without time zone,
    data json,
    datasetversion_id bigint NOT NULL,
    datapoint_id bigint NOT NULL
);

ALTER TABLE ONLY datasetversion_datapoint
    ADD CONSTRAINT datasetversion_datapoint_ext_id_key UNIQUE (ext_id);

ALTER TABLE ONLY datasetversion_datapoint
    ADD CONSTRAINT datasetversion_datapoint_pkey PRIMARY KEY (id);

CREATE SEQUENCE datasetversion_datapoint_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE datasetversion_datapoint_id_seq OWNED BY datasetversion_datapoint.id;

ALTER TABLE ONLY datasetversion_datapoint ALTER COLUMN id SET DEFAULT nextval('datasetversion_datapoint_id_seq'::regclass);

ALTER TABLE ONLY datasetversion_datapoint
    ADD CONSTRAINT datasetversion_datapoint_datasetversion_id_fkey FOREIGN KEY (datasetversion_id) REFERENCES datasetversion(id);

ALTER TABLE ONLY datasetversion_datapoint
    ADD CONSTRAINT datasetversion_datapoint_datapoint_id_fkey FOREIGN KEY (datapoint_id) REFERENCES datapoint(id);

-- a datapoint can only be mapped to a dataset version once
CREATE UNIQUE INDEX ix_datasetversion_datapoint_unique ON datasetversion_datapoint USING BTREE (datasetversion_id, datapoint_id);
CREATE INDEX ix_datasetversion_datapoint_created_at ON datasetversion_datapoint USING BTREE (created_at);
CREATE INDEX ix_datasetversion_datapoint_updated_at ON datasetversion_datapoint USING BTREE (updated_at);
CREATE INDEX ix_datasetversion_datapoint_deleted_at ON datasetversion_datapoint USING BTREE (deleted_at);

-- models for role-based access concept

CREATE TYPE obj_role AS ENUM ('superuser', 'admin', 'developer', 'viewer', 'auditor');

-- object roles for organizations
CREATE TABLE object_role (
    id bigint NOT NULL,
    ext_id uuid NOT NULL,
    object_id uuid NOT NULL,
    organization_id uuid NOT NULL,
    organization_role CHARACTER VARYING NOT NULL, --the role in the organization
    object_type CHARACTER VARYING NOT NULL,
    object_role obj_role NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc', now()),
    deleted_at TIMESTAMP WITH TIME ZONE
);

ALTER TABLE ONLY object_role
    ADD CONSTRAINT object_role_pkey PRIMARY KEY (id);

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

CREATE UNIQUE INDEX ix_object_role_unique ON object_role (object_id, organization_id, organization_role);
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
