-- Populate status_user
insert into status_user (uuid, status_user, description) values (gen_random_uuid(), 'Pending review','The documents are being checking');
insert into status_user (uuid, status_user, description) values (gen_random_uuid(), 'Approved','User verified documents');
insert into status_user (uuid, status_user, description) values (gen_random_uuid(), 'Rejected','Rejected for false documentation');

-- Populate status_file
INSERT INTO status_file (uuid, status_user, description) VALUES (gen_random_uuid(), 'Pending review','The file is being checking');
INSERT INTO status_file (uuid, status_user, description) VALUES (gen_random_uuid(), 'Approved','File approved');
INSERT INTO status_file (uuid, status_user, description) VALUES (gen_random_uuid(), 'Rejected','File rejected');

-- Populate status_product
INSERT INTO status_product (uuid, status_product, description) VALUES (gen_random_uuid(), 'Pending review','Product is being checking');
INSERT INTO status_product (uuid, status_product, description) VALUES (gen_random_uuid(), 'Approved','Product is approved');
INSERT INTO status_product (uuid, status_product, description) VALUES (gen_random_uuid(), 'Rejected','Product is rejected');

-- Populate profile_images
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'astronaut-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-s.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'astronaut-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-m.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'astronaut-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/astronaut-b.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'woman1-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/woman1-s.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'woman1-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/woman1-m.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'woman1-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/woman1-b.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'dad-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/dad-s.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'dad-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/dad-m.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'dad-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/dad-b.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'beard-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/beard-s.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'beard-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/beard-m.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'beard-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/beard-b.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'serious-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/serious-s.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'serious-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/serious-m.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'serious-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/serious-b.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'woman2-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/woman2-s.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'woman2-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/woman2-m.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'woman2-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/woman2-b.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'hat1-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/hat1-s.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'hat1-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/hat1-m.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'hat1-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/hat1-b.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'woman3-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/woman3-s.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'woman3-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/woman3-m.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'woman3-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/woman3-b.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'hat2-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/hat2-s.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'hat2-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/hat2-m.png');
INSERT INTO profile_images (uuid, image_name, format, image_url) VALUES(gen_random_uuid(), 'hat2-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/hat2-b.png');

-- Populate Basic Products
INSERT INTO basic_products (uuid, basic_product) VALUES(gen_random_uuid(), 'Coffe');
INSERT INTO basic_products (uuid, basic_product) VALUES(gen_random_uuid(), 'Cocoa');
INSERT INTO basic_products (uuid, basic_product) VALUES(gen_random_uuid(), 'Avocado');

-- Populate Product Types
INSERT INTO products_type (uuid, product_type, basic_product_id) VALUES(gen_random_uuid(), 'Beans', 1);
INSERT INTO products_type (uuid, product_type, basic_product_id) VALUES(gen_random_uuid(), 'Beans rosted', 1);
INSERT INTO products_type (uuid, product_type, basic_product_id) VALUES(gen_random_uuid(), 'Packaged', 1);

INSERT INTO products_type (uuid, product_type, basic_product_id) VALUES(gen_random_uuid(), 'Beans', 2);
INSERT INTO products_type (uuid, product_type, basic_product_id) VALUES(gen_random_uuid(), 'Beans rosted', 2);
INSERT INTO products_type (uuid, product_type, basic_product_id) VALUES(gen_random_uuid(), 'Packaged', 2);

INSERT INTO products_type (uuid, product_type, basic_product_id) VALUES(gen_random_uuid(), 'Fruits', 3);

-- Populate varieties
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Arabica coffe',1);
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Robusta coffe',1);

INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Forastero',2);
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Criollo',2);
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Trinitario',2);

INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Hass',3);
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Lamb Hass',3);
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Pinkerton',3);
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Reed',3);
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Carmen',3);

-- Populate sustainability certifications
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'ISO 14001');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'ECO-OK');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'Global GAP');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'SA8000');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'EUREPGAP');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'SAI-Platform');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'Rainforest Alliance');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'HACCP');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'SASA - Platform');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'BASC');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'COLEACP');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'No certificate');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'ICA BPA');
INSERT INTO sustainability_certifications (uuid, certification) VALUES(gen_random_uuid(), 'Other');

-- Populate incoterms
INSERT INTO incoterms (uuid, incoterm) VALUES(gen_random_uuid(), 'Delivery at place (DAP)');
INSERT INTO incoterms (uuid, incoterm) VALUES(gen_random_uuid(), 'Free on board (FOB)');
INSERT INTO incoterms (uuid, incoterm) VALUES(gen_random_uuid(), 'Cost, insurance and freight (CIF)');
INSERT INTO incoterms (uuid, incoterm) VALUES(gen_random_uuid(), 'Ex works (EXW)');

-- Populate minimums_order
INSERT INTO minimums_order (uuid, minimum_order) VALUES(gen_random_uuid(), 'Bags (DHL)');
INSERT INTO minimums_order (uuid, minimum_order) VALUES(gen_random_uuid(), 'A Continer');
INSERT INTO minimums_order (uuid, minimum_order) VALUES(gen_random_uuid(), 'Multiple Continers');







