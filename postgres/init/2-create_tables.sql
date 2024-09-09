-- book definition

-- Drop book
-- DROP TABLE book;

CREATE TABLE book (
	id serial NOT NULL,
	"title" text NOT NULL,
	publish_date text NULL,
	"lang" text NULL,
	"series" text NULL,
	"note" text NULL,
	CONSTRAINT book_pk PRIMARY KEY (id)
);