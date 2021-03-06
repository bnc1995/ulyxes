-- tables for Ulyxes monitoring
-- spatialite version
-- create a new empty spatialite database first

-- table for points with web mercator geometry
-- each point must be inserted into this table
-- it is used to display points on web map (EPSG:3857)
-- ptype can be FIX/STA/MON for fix points, stations, monitoring points
-- code can be ATR/RLA/PR/RL/ORI
-- pc additive constant for distance measurement
CREATE TABLE monitoring_poi (
	id varchar(50) PRIMARY KEY,
	ptype char(3) NOT NULL DEFAULT 'MON' CHECK (ptype in ('FIX','STA','MON')),
	code char(4) NOT NULL DEFAULT 'ATR' CHECK (code in ('ATR', 'PR', 'ORI', 'RL', 'RLA')),
	pc float NOT NULL DEFAULT 0
);
SELECT AddGeometryColumn('monitoring_poi', 'geom', 3857, 'POINT', 3);

-- table for point coordinates in local reference system
-- coordinates calculated by Ulyxes
CREATE TABLE monitoring_coo (
	id varchar(50) NOT NULL REFERENCES monitoring_poi(id),
	east double precision NOT NULL,
	north double precision NOT NULL,
	elev double precision NOT NULL,
	datetime timestamp NOT NULL,
	CONSTRAINT pkey_coo PRIMARY KEY (id, datetime)
);

-- table for observations
-- polar observations made by Ulyxes
CREATE TABLE monitoring_obs (
	id varchar(50) NOT NULL REFERENCES monitoring_poi(id),
	hz double precision NOT NULL,
	v double precision NOT NULL,
	distance double precision,
	crossincline double precision,
	lengthincline double precision,
    datetime timestamp NOT NULL,
	CONSTRAINT pkey_obs PRIMARY KEY (id, datetime)
);

-- table for meteorological observations at stations
-- id point id for observation
-- temp temperature celsius
-- pressure air pressure hpa
-- humidity
-- wettemp wet temperature
-- datetime of observation
CREATE TABLE monitoring_met (
	id varchar(50) NOT NULL REFERENCES monitoring_poi(id),
	temp double precision NOT NULL,
	pressure double precision NOT NULL,
	humidity double precision,
	wettemp double precision,
    datetime timestamp NOT NULL,
	CONSTRAINT pkey_m PRIMARY KEY (id, datetime)
);

-- table for extra info
-- datetime of observation
-- nref number of reference points
-- nrefobs number of reference points measured
-- nmon number of monitoring points
-- nmonobs number of monitoring points measured
CREATE TABLE monitoring_inf (
    datetime timestamp NOT NULL,
	nref integer,
	nrefobs integer,
	nmon integer,
	nmonobs integer,
	maxincl double precision,
	std_east double precision,
	std_north double precision,
	std_elev double precision,
	std_ori double precision,
	CONSTRAINT pkey_i PRIMARY KEY (datetime)
);

-- table for point groups
-- id name of group
-- remark optional description of group
CREATE TABLE monitoring_grp (
	id varchar(50) PRIMARY KEY,
	remark varchar(100)
);

-- table for point group connections
-- gid group id
-- pid point id
CREATE TABLE monitoring_pgr (
	gid varchar(50) NOT NULL REFERENCES monitoring_grp(id),
	pid varchar(50) NOT NULL REFERENCES monitoring_poi(id),
	CONSTRAINT pkey_pgr PRIMARY KEY (gid, pid)
);

