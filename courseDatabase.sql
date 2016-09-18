drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  courseNumber text not null,
  courseName text not null,
  courseBit boolean not null
);