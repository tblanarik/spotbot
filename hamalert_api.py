import os
import requests
import logging
import json
from typing import Dict, List, Optional


class HamAlertAPI:
    """Client for interacting with HamAlert's API."""

    LOGIN_URL = "https://hamalert.org/login"
    TRIGGERS_URL = "https://hamalert.org/ajax/triggers"
    TRIGGER_UPDATE_URL = "https://hamalert.org/ajax/trigger_update"

    def __init__(self):
        self.username = os.environ.get('HAMALERT_USERNAME')
        self.password = os.environ.get('HAMALERT_PASSWORD')
        self.session = None

        if not self.username or not self.password:
            raise ValueError("HAMALERT_USERNAME and HAMALERT_PASSWORD environment variables must be set")

    def login(self) -> bool:
        """
        Authenticate with HamAlert and establish a session.

        Returns:
            bool: True if login successful, False otherwise
        """
        self.session = requests.Session()

        try:
            response = self.session.post(
                self.LOGIN_URL,
                data={
                    'username': self.username,
                    'password': self.password
                }
            )

            # Check if login was successful
            # HamAlert typically redirects or sets cookies on success
            if response.status_code == 200 and self.session.cookies:
                logging.info("Successfully logged in to HamAlert")
                return True
            else:
                logging.error(f"Login failed with status code: {response.status_code}")
                return False

        except Exception as e:
            logging.error(f"Error during HamAlert login: {e}")
            return False

    def get_triggers(self) -> Optional[List[Dict]]:
        """
        Fetch all configured triggers from HamAlert.

        Returns:
            Optional[List[Dict]]: List of trigger objects, or None if request failed
        """
        if not self.session:
            if not self.login():
                return None

        try:
            response = self.session.get(self.TRIGGERS_URL)

            if response.status_code == 200:
                return response.json()
            else:
                logging.error(f"Failed to fetch triggers: {response.status_code}")
                # Try logging in again in case session expired
                if self.login():
                    response = self.session.get(self.TRIGGERS_URL)
                    if response.status_code == 200:
                        return response.json()
                return None

        except Exception as e:
            logging.error(f"Error fetching triggers: {e}")
            return None

    def add_trigger(self, conditions: Dict, comment: str = "") -> Optional[Dict]:
        """
        Add a new trigger to HamAlert.

        Args:
            conditions: Dictionary of condition types and values
            comment: Optional comment for the trigger

        Returns:
            Optional[Dict]: Response from HamAlert, or None if request failed
        """
        if not self.session:
            if not self.login():
                return None

        data = {
            'conditions': conditions,
            'actions': ["url"],
            'comment': comment,
            'options': {},
        }

        try:
            response = self.session.post(
                self.TRIGGER_UPDATE_URL,
                json=data,
            )

            if response.status_code == 200:
                logging.info(f"Successfully added trigger: {comment}")
                return response.json()

            logging.error(f"Failed to add trigger: {response.status_code} - {response.text}")

            # Try logging in again in case session expired
            if self.login():
                response = self.session.post(
                    self.TRIGGER_UPDATE_URL,
                    json=data,
                )
                if response.status_code == 200:
                    return response.json()
            return None

        except Exception as e:
            logging.error(f"Error adding trigger: {e}")
            return None
