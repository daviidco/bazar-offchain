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
INSERT INTO status_product (uuid, status_product, description) VALUES (gen_random_uuid(), 'Approved','Product is approved by admin');
INSERT INTO status_product (uuid, status_product, description) VALUES (gen_random_uuid(), 'Rejected','Product is rejected by admin');
INSERT INTO status_product (uuid, status_product, description) VALUES (gen_random_uuid(), 'Published','Product is visible to buyers and is a operation by seller');
INSERT INTO status_product (uuid, status_product, description) VALUES (gen_random_uuid(), 'Hidden','Product is hidden to buyers and is a default state when product is edited or when product has not certifications');
INSERT INTO status_product (uuid, status_product, description) VALUES (gen_random_uuid(), 'Deleted','Product has a logic deleted');

-- Populate profile_images
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(1, '0860ee2b-b689-4618-9087-de6bac1a054e', 'Avatar1-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar1-s.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(2, '7df80df2-2d99-4a5b-94db-2c70d37fe01a', 'Avatar1-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar1-m.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(3, 'eb0f168e-b5d7-4abe-aaad-57c34bdbc77c', 'Avatar1-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar1-b.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(4, 'ae3f4122-9a53-4838-a100-b533a2cc8390', 'Avatar2-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar2-s.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(5, '9e36840e-d88a-41f4-ae09-f498fa86f401', 'Avatar2-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar2-m.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(6, 'd0d73da3-2567-4a4c-b5b5-c6d994fde16f', 'Avatar2-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar2-b.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(7, '77f5c209-b7b7-45fb-955a-da3241f50cf3', 'Avatar3-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar3-s.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(8, '788d44aa-ea04-4554-93cb-0b84eb908c37', 'Avatar3-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar3-m.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(9, '7dd06cd7-2fc0-476f-8555-2a74e29b2962', 'Avatar3-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar3-b.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(10, 'cdac11d6-25d3-4864-81b4-a0db5cb8a47c', 'Avatar4-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar4-s.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(11, 'aabc0a37-8e6d-48a4-a434-f4fc27d8ccb4', 'Avatar4-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar4-m.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(12, 'b60c0732-863c-4500-ae79-68df0f1e148e', 'Avatar4-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar4-b.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(13, '8d0e923c-6ce0-4f4a-9dd5-0aca627f7701', 'Avatar5-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar5-s.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(14, '347b3c65-5fee-4106-b9ce-5d5cc3c37186', 'Avatar5-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar5-m.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(15, '60ee02fb-c85c-4222-b632-a8bdc023ed51', 'Avatar5-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar5-b.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(16, 'a698a750-feae-404c-838d-8d6a92fefaff', 'Avatar6-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar6-s.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(17, '17cc4485-6382-429e-a810-e704c1215ab3', 'Avatar6-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar6-m.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(18, '8f30eb9f-fa73-496a-9fcb-1aab0242f40a', 'Avatar6-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar6-b.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(19, '0e329595-4119-4d7f-9e6b-526c15bae949', 'Avatar7-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar7-s.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(20, '5bcf45a0-fb0c-45d4-9cb7-6e87adc3d2e2', 'Avatar7-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar7-m.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(21, '08f246fc-8d3d-46a4-9e9f-8a39a7358029', 'Avatar7-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar7-b.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(22, '399f1770-f46d-46c4-b8c6-4da2605a0822', 'Avatar8-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar8-s.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(23, '7fea7544-adbf-4531-ad49-c012963ff194', 'Avatar8-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar8-m.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(24, '8e6f4b81-ece8-42e1-8280-9ee564640450', 'Avatar8-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar8-b.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(25, '7ed1e388-84fe-4962-ad96-e64dfd713607', 'Avatar9-s', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar9-s.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(26, '4686a116-ac93-4637-9c2f-9b5f8b9a62d7', 'Avatar9-m', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar9-m.png');
INSERT INTO profile_images (id, uuid, image_name, format, image_url) VALUES(27, '3516c1f9-b649-4772-bcae-3ce888000e07', 'Avatar9-b', 'png', 'https://s3-offchain-test.s3.us-east-2.amazonaws.com/profile_images/Avatar9-b.png');


-- Populate Basic Products
INSERT INTO basic_products (uuid, basic_product) VALUES(gen_random_uuid(), 'Coffee');
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
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Arabica coffee',1);
INSERT INTO varieties (uuid, variety, basic_product_id) VALUES(gen_random_uuid(), 'Robusta coffee',1);

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
INSERT INTO minimums_order (uuid, minimum_order) VALUES(gen_random_uuid(), 'A Container');
INSERT INTO minimums_order (uuid, minimum_order) VALUES(gen_random_uuid(), 'Multiple Containers');







