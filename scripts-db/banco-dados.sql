-- tabela que armazena os dados de local de plancacao
create table t_local (cd_local integer auto_increment not null primary key, nm_local varchar(50) not null);
-- dados de exemplo de localizações de plantação
insert into t_local (nm_local) values ('Plantacao Cafe 01');
insert into t_local (nm_local) values ('Plantacao Soja 02');

-- tabela que armazena os sensores instalados em cada local de plantacao
create table t_sensor (cd_sensor integer not null auto_increment primary key, cd_local integer not null, nm_sensor varchar(35) not null);
-- associacao entre sensores e locais de plantacao
alter table t_sensor add constraint fk_local foreign key (cd_local) references t_local(cd_local);
-- dados de exemplo de sensores instalados
insert into t_sensor (cd_local, nm_sensor) values (1, 'Sensor Fosforo');
insert into t_sensor (cd_local, nm_sensor) values (1, 'Sensor Potassio');
insert into t_sensor (cd_local, nm_sensor) values (2, 'Sensor pH');
insert into t_sensor (cd_local, nm_sensor) values (2, 'Sensor Umidade');

-- tabela que registra os dados coletados pelos sensores
create table t_coleta (ts_coleta timestamp not null, cd_sensor integer not null, vl_coleta double not null, tp_indicador varchar(20) not null);
-- definindo a chave primaria como composta garantindo que nao seja coletada no mesmo momento dados do mesmo sensor
alter table t_coleta add primary key (ts_coleta, cd_sensor);
-- associacao entre dados coletados e sensores
alter table t_coleta add constraint fk_sensor foreign key (cd_sensor) references t_sensor(cd_sensor);


-- tabela que armazena os dados de produtos que podem ser administrados na plantacao
create table t_produto (cd_produto integer not null auto_increment primary key, ds_produto varchar(50) not null);
-- dados de exemplo de produtos
insert into t_produto (ds_produto) values ('Adubo NPK 10-10-10');
insert into t_produto (ds_produto) values ('Iririgacao');

-- tabela que armazena os dados dos produtos adminsitrados em cada local de plantacao
create table t_aplicacao (ts_aplicacao timestamp not null, cd_produto integer not null, cd_local integer not null,qt_produto double);
-- definindo a chave primaria como composta garantindo que nao seja administrado o mesmo produto no mesmo momento
alter table t_aplicacao add primary key (ts_aplicacao, cd_produto, cd_local);
-- associacao entre produtos administrados e locais de plantacao
alter table t_aplicacao add constraint fk_local_aplicacao foreign key (cd_local) references t_local(cd_local);
-- associacao entre produtos administrados e produtos   
alter table t_aplicacao add constraint fk_produto foreign key (cd_produto) references t_produto(cd_produto);


