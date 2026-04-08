"""Geocoding service for location-based ranking."""

import time
import math
from typing import Optional, Tuple
from datetime import datetime, timezone, timedelta
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError


class GeocodingService:
    """Service for geocoding locations and calculating distances."""

    # Locations that indicate remote work
    REMOTE_KEYWORDS = [
        'remote',
        'remote work',
        'anywhere',
        'virtual',
        'work from home',
        'wfh',
        'distributed',
        'work anywhere'
    ]

    def __init__(self):
        """Initialize geocoding service with rate limiting."""
        self.geocoder = Nominatim(user_agent="roleradar/2.0")
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Nominatim requires 1 req/sec
        self.cache_duration_days = 90  # Re-geocode after 90 days

    def _rate_limit(self):
        """Enforce rate limiting for Nominatim."""
        now = time.time()
        elapsed = now - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()

    @staticmethod
    def is_remote_location(location: str) -> bool:
        """
        Check if a location indicates remote work.

        Args:
            location: Location string to check

        Returns:
            True if location indicates remote work, False otherwise
        """
        if not location or not location.strip():
            return False

        location_lower = location.lower().strip()
        return any(keyword in location_lower for keyword in GeocodingService.REMOTE_KEYWORDS)

    def geocode(self, location: str) -> Optional[Tuple[float, float]]:
        """
        Geocode a location string to coordinates.

        Args:
            location: Location string (e.g., "San Francisco, CA", "Remote")

        Returns:
            Tuple of (latitude, longitude) or None if geocoding fails
        """
        if not location or not location.strip():
            return None

        # Handle "Remote" locations
        if self.is_remote_location(location):
            return None

        try:
            self._rate_limit()
            result = self.geocoder.geocode(location, timeout=10)

            if result:
                return (result.latitude, result.longitude)
            return None

        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Geocoding timeout/service error for '{location}': {e}")
            return None
        except Exception as e:
            print(f"Unexpected geocoding error for '{location}': {e}")
            return None

    def should_geocode(self, geocoded_at: Optional[datetime]) -> bool:
        """
        Check if a location should be re-geocoded based on cache age.

        Args:
            geocoded_at: Timestamp when location was last geocoded

        Returns:
            True if should re-geocode, False otherwise
        """
        if not geocoded_at:
            return True

        # Handle both aware and naive datetimes
        if geocoded_at.tzinfo is None:
            geocoded_at = geocoded_at.replace(tzinfo=timezone.utc)

        age = datetime.now(timezone.utc) - geocoded_at
        return age > timedelta(days=self.cache_duration_days)

    def calculate_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculate distance between two points using Haversine formula.

        Args:
            lat1, lon1: First point coordinates (user location)
            lat2, lon2: Second point coordinates (opportunity location)

        Returns:
            Distance in miles
        """
        # Earth radius in miles
        R = 3959.0

        # Convert to radians
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        # Haversine formula
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    def score_distance(
        self,
        distance_miles: float,
        max_distance: float = 500.0
    ) -> float:
        """
        Convert distance to a score between 0 and 1.
        Closer locations score higher.

        Args:
            distance_miles: Distance in miles
            max_distance: Maximum effective distance (default 500 miles)

        Returns:
            Score between 0 and 1 (1.0 = closest, 0.0 = too far)
        """
        if distance_miles <= 0:
            return 1.0

        if distance_miles >= max_distance:
            return 0.0

        # Inverse linear scoring: 1.0 at 0 miles, 0.0 at max_distance
        return 1.0 - (distance_miles / max_distance)

    def get_distance_category(self, distance_miles: float) -> str:
        """
        Categorize distance for human-readable display.

        Args:
            distance_miles: Distance in miles

        Returns:
            Category string: "Local", "Regional", "Distant", "Very Distant"
        """
        if distance_miles < 50:
            return "Local"
        elif distance_miles < 250:
            return "Regional"
        elif distance_miles < 500:
            return "Distant"
        else:
            return "Very Distant"
