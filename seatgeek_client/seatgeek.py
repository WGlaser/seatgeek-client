"""
A simple Seatgeek Python Client to retrieve ticket info
"""

from typing import List

import requests


class SeatGeek:
    """
    A simple client for wrapping the SeatGeek API

    Attributes:
        BASE_API_URL: The URL of the Seatgeek API
    """

    BASE_API_URL = "https://api.seatgeek.com/2"

    def __init__(
        self, client_id: str, client_secret: str, user_agent: str | None = None
    ) -> None:
        self.session = self._establish_session(
            client_id, client_secret, user_agent=user_agent
        )
        self.api_url = self.BASE_API_URL

    def _establish_session(
        self, client_id: str, client_secret: str, user_agent: str | None
    ) -> requests.Session:
        """For creating an authetnicated session with the Seatgeek API

        Args:
            client_id (str): client ID from seatgeek API
            client_secret (str): client secret from seatgeek API

        Returns:
            requests.Session: an authenticated API session
        """
        headers = {}
        if user_agent:
            headers["User-Agent"] = user_agent
        headers["Accept"] = "application/json"

        session = requests.Session()
        session.auth = (client_id, client_secret)
        session.headers.update(headers)
        return session

    def get_events(
        self,
        performer_by_slug: List[dict[str, str]] | None = None,
        performer_by_id: List[dict[int, str]] | None = None,
        multiple_performers_or: bool | None = None,
        venues: List[dict[str, str, int]] | None = None,
        multiple_venues_or: bool | None = None,
        datetime: dict[str, str] | None = None,
        query: str | None = None,
        taxonomies: List[dict[int, str, int]] | None = None,
    ) -> dict:
        """The performers argument is used to scope the result set to specific
          performers. The performers argument may be used several times
          in the same query.

        Args:
            performer_slug (List[dict[str, str]], optional): A dictionary of team names
              in the form 'Boston-Celtcs', and a specificity string. Valid values for
              specificty are : home_team, away_team, primary, any.
              Defaults to None | None.

            performer_id (List[dict[int, str]], optional): A dictionary of team IDs
              and a specificity string. Valid values for specificty are : home_team,
              away_team, primary, any.  Defaults to None | None.

            multiple_performers_or (bool, optional): Boolean if you want
            to search for multiple events with OR operator. Must use
            performer IDs only. Defaults to None | None.

            venues (List[dict[str,str,int]], optional): List of dictionaries, with
            each entry representing a venue in City, ID, State order.

            multiple_venues_or (bool, optional): Boolean if you want
            to search for multiple venues with OR operator. Must use
            venue IDs only. Defaults to None | None.

            datetime (dict[str, str], option): The datetime argument is used to scope
            the result set to events occurring within a certain date and time range.
            The datetime argument may be used zero, one, or two times in a query.
            You can scope the date to a range using operators gt, gte, lt, and lte.
            Dictionary format is {Date: 'YYYY-MM-DD' format, str: operator}. No
            operator will result in an exact date match.

            query (str, optional):

            taxonomies (List[dict[int,str,int]], optional):
        Returns:
            dict: _description_
        """
        params = {}

        if performer_by_slug:
            for item in performer_by_slug:
                if item["specificity"] is not None:
                    params.setdefault(
                        f'performers[{item["specificity"]}].slug', []
                    ).append(item["slug"])
                else:
                    params.setdefault("performers.slug", []).append(item["slug"])

        if performer_by_id:
            for item in performer_by_id:
                if item["specificity"] is not None:
                    params[f'performers[{item["specificity"]}].id'] = item["id"]
                else:
                    params.setdefault("performers.id", []).append(item["id"])

        if multiple_performers_or:
            for key, value in params.items():
                if type(value) is list and key == "performers.id":
                    params.update({key: ",".join(value)})

        if venues:
            if multiple_venues_or:
                # add only venue IDs
                for venue in venues:
                    params.setdefault("venue.id", []).append(venue["id"])
                # turn it into a comma seperated list
                for key, value in params.items():
                    if type(value) is list and key == "venue.id":
                        params.update({key: ",".join(str(i) for i in value)})
            else:
                for venue in venues:
                    for key, val in venue.items():
                        if val is not None:
                            params.setdefault(f"venue.{key}", []).append(val)

        if datetime:
            for data in datetime:
                if data["operator"] is not None:
                    params.setdefault(f'datetime_local.{data["operator"]}', []).append(
                        data["date"]
                    )
                else:
                    params.setdefault("datetime_local", []).append(data["date"])

        print(params)
        resp = self.session.get(f"{self.BASE_API_URL}/events", params=params)
        print(resp.url)
        return resp.json()

    def get_performers(
        self,
        slug: str | None = None,
        id: int | None = None,
        query: str | None = None,
        taxonomies: str | None = None,
        genres: str | None = None,
    ) -> dict:
        """
        To find a performer matching your search criteria you will send a request to
        the /performers endpoint. Sending a request to /performers will return a
        paginated list of all performers.

        All arguments can be used with each other with the exception of the id argument.
        id can only be used with API-wide arguments, such as those for pagination
        and sorting.

        Args:
            slug (str | None, optional): _description_. Defaults to None.
            id (int | None, optional): _description_. Defaults to None.

        Returns:
            dict: _description_
        """

        params = {
            "slug": slug,
            "id": id,
            "query": query,
            "taxonomies": taxonomies,
            "genres": genres,
        }

        resp = self.session.get(f"{self.BASE_API_URL}/performers", params=params)

        return resp.json()
