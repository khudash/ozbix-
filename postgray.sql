-- ============================================================
-- OZBION / OZEBIX POSTGRESQL DATABASE INITIALIZATION & SCHEMA
-- Database: ozbix_db
-- File: postgray.sql
-- ============================================================

-- Step 1: Create Database & Connect (Run in psql or pgAdmin)
-- CREATE DATABASE ozbix_db WITH OWNER postgres ENCODING 'UTF8';
-- \c ozbix_db;

-- Step 2: Drop existing tables if re-initializing
DROP TABLE IF EXISTS website_contactsubmission CASCADE;
DROP TABLE IF EXISTS website_client CASCADE;
DROP TABLE IF EXISTS website_ozbixfolio CASCADE;
DROP TABLE IF EXISTS website_service CASCADE;
DROP TABLE IF EXISTS website_banner CASCADE;
DROP TABLE IF EXISTS django_admin_log CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions CASCADE;
DROP TABLE IF EXISTS auth_user_groups CASCADE;
DROP TABLE IF EXISTS auth_group_permissions CASCADE;
DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;

-- Step 3: Create Tables Schema for PostgreSQL

-- Django Auth & System Tables
CREATE TABLE django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model)
);

CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE website_banner (
    id SERIAL PRIMARY KEY,
    image VARCHAR(100) NOT NULL
);

CREATE TABLE website_service (
    id SERIAL PRIMARY KEY,
    icon_class VARCHAR(100) NOT NULL,
    title VARCHAR(100) NOT NULL,
    short_description VARCHAR(150) NOT NULL,
    description TEXT NOT NULL,
    button_text VARCHAR(50) NOT NULL DEFAULT 'Read More'
);

CREATE TABLE website_ozbixfolio (
    id SERIAL PRIMARY KEY,
    image VARCHAR(100) NOT NULL,
    title VARCHAR(100) NOT NULL
);

CREATE TABLE website_client (
    id SERIAL PRIMARY KEY,
    image VARCHAR(100) NOT NULL
);

CREATE TABLE website_contactsubmission (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    phone VARCHAR(50) NULL,
    services VARCHAR(255) NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Step 4: Seed Data for Ozbix Website Services & Content
INSERT INTO website_service (icon_class, title, short_description, description, button_text) VALUES
('fas fa-shopping-cart', 'Shopify Development', 'Custom Shopify Store Creation & Optimization', 'Build scalable, high-converting e-commerce websites with custom themes and app integrations.', 'Explore Shopify'),
('fab fa-wordpress', 'WordPress Solutions', 'Custom Themes, Plugins & Speed Optimization', 'Enterprise-level WordPress development tailored to business requirements with security and high performance.', 'Explore WordPress'),
('fas fa-laptop-code', 'Web Design & Frontend', 'Modern Responsive Web Applications', 'Stunning user interface designs and interactive web app development using latest frontend frameworks.', 'View Web Design'),
('fas fa-search-dollar', 'SEO & Digital Marketing', 'Search Engine Ranking & Brand Growth', 'Comprehensive SEO strategies, technical auditing, and content optimization to drive organic traffic.', 'Learn SEO');

INSERT INTO website_contactsubmission (full_name, email, phone, services, message, is_read, created_at) VALUES
('John Doe', 'john@example.com', '+1 555 0192', 'Shopify Development, Web Design', 'Hello! I need a custom Shopify e-commerce store built for my retail brand.', false, NOW() - INTERVAL '2 days'),
('Sarah Smith', 'sarah@designagency.io', '+44 7700 900077', 'WordPress Solutions', 'Looking for custom WordPress theme optimization and page speed boost.', false, NOW() - INTERVAL '1 day'),
('Ali Khan', 'ali.khan@techcorp.pk', '+92 300 1234567', 'SEO & Digital Marketing', 'We want to increase our search engine rankings and launch Google Ads campaign.', true, NOW());

-- Confirmation message
SELECT 'Ozbix PostgreSQL database schema and seed data created successfully!' AS status;
