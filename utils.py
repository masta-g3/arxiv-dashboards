from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
import psycopg2
import re
import os
import uuid

db_params = {}
try:
    db_params = {
        "dbname": os.environ["DB_NAME"],
        "user": os.environ["DB_USER"],
        "password": os.environ["DB_PASS"],
        "host": os.environ["DB_HOST"],
        "port": os.environ["DB_PORT"],
    }
except:
    db_params = {**st.secrets["postgres"]}


database_url = f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['dbname']}"


def get_img_link_for_blob(text_blob: str):
    """Identify `arxiv_code from a text blob, and generate a Markdown link to its img."""
    arxiv_code = re.findall(r"arxiv:(\d{4}\.\d{4,5})", text_blob)
    if len(arxiv_code) == 0:
        return None
    arxiv_code = arxiv_code[0]
    return f"https://llmpedia.s3.amazonaws.com/{arxiv_code}.png"


def get_arxiv_title_dict():
    """Get a list of all arxiv titles in the database."""
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
            SELECT a.arxiv_code, a.title 
            FROM arxiv_details a
            WHERE a.title IS NOT NULL
            """
            )
            title_map = {row[0]: row[1] for row in cur.fetchall()}
            return title_map


def get_recursive_summary(arxiv_code: str) -> str:
    """Get recursive summary for a given arxiv code."""
    engine = create_engine(database_url)
    with engine.begin() as conn:
        query = text(
            f"""
            SELECT arxiv_code, summary
            FROM recursive_summaries
            WHERE arxiv_code = '{arxiv_code}';
            """
        )
        result = conn.execute(query)
        summary = result.fetchone()
    engine.dispose()
    result = summary[1] if summary else None
    return result


def get_extended_notes(arxiv_code: str, level=None, expected_tokens=None):
    """Get extended summary for a given arxiv code."""
    engine = create_engine(database_url)
    with engine.begin() as conn:
        if level:
            query = text(
                f"""
                SELECT arxiv_code, level, summary
                FROM summary_notes
                WHERE arxiv_code = '{arxiv_code}'
                AND level = '{level}';
                """
            )
        elif expected_tokens:
            query = text(
                f"""
                SELECT DISTINCT ON (arxiv_code) arxiv_code, level, summary, tokens
                FROM summary_notes
                WHERE arxiv_code = '{arxiv_code}'
                ORDER BY arxiv_code, ABS(tokens - {expected_tokens}) ASC;
                """
            )
        else:
            query = text(
                f"""
                SELECT DISTINCT ON (arxiv_code) arxiv_code, level, summary
                FROM summary_notes
                WHERE arxiv_code = '{arxiv_code}'
                ORDER BY arxiv_code, level DESC;
                """
            )
        result = conn.execute(query)
        summary = result.fetchone()
    engine.dispose()
    return summary[2]


def log_request(arxiv_code: str) -> bool:
    """Log Q&A in DB along with streamlit app state."""
    try:
        engine = create_engine(database_url)
        with engine.begin() as conn:
            request_id = str(uuid.uuid4())
            tstp = pd.to_datetime("now").strftime("%Y-%m-%d %H:%M:%S")
            query = text(
                """
                INSERT INTO dashboard_requests (request_id, tstp, arxiv_code)
                VALUES (:request_id, :tstp, :arxiv_code)
            """
            )
            conn.execute(
                query,
                {
                    "request_id": request_id,
                    "tstp": tstp,
                    "arxiv_code": arxiv_code,
                },
            )
    except Exception as e:
        print(f"Error in logging visit: {e}")
        return False
    return True


def get_daily_arxiv_request_count(date_str: str) -> int:
    """Get the number of requests for a given date."""
    engine = create_engine(database_url)
    with engine.begin() as conn:
        query = text(
            f"""
            SELECT COUNT(DISTINCT arxiv_code)
            FROM arxiv_dashboards
            WHERE tstp::date = '{date_str}';
            """
        )
        result = conn.execute(query)
        count = result.fetchone()[0]
    engine.dispose()
    return count


def get_arxiv_dashboard_script(arxiv_code: str, sel_col: str = "script_content") -> str:
    """Query DB to get script for the arxiv dashboard."""
    engine = create_engine(database_url)
    with engine.begin() as conn:
        query = text(
            f"""
            SELECT {sel_col}
            FROM arxiv_dashboards
            WHERE arxiv_code = '{arxiv_code}';
            """
        )
        result = conn.execute(query)
        row = result.fetchone()
        script = row[0] if row else None
    engine.dispose()
    return script

def save_arxiv_dashboard_script(arxiv_code: str, summary:str, script: str) -> bool:
    """Insert a new arxiv dashboard script into the DB."""
    engine = create_engine(database_url)
    tstp = pd.to_datetime("now").strftime("%Y-%m-%d %H:%M:%S")
    with engine.begin() as conn:
        query = text(
            """
            INSERT INTO arxiv_dashboards (arxiv_code, tstp, script_content, summary)
            VALUES (:arxiv_code, :tstp, :script_content, :summary)
            """
        )
        conn.execute(
            query,
            {
                "arxiv_code": arxiv_code,
                "tstp": tstp,
                "script_content": script,
                "summary": summary,
            },
        )
        return True