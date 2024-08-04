
CREATE TABLE models (
	id INT AUTO_INCREMENT,
	model_name varchar(250),
	model_version varchar(250),
    model_size varchar(250),
	model_created varchar(250),
	model_source varchar(250),
    model_variant varchar(250),
	model_path varchar(250),
    model_str varchar(250),
	model_description LONGTEXT,
	PRIMARY KEY (id)
);
