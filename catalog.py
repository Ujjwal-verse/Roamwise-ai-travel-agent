"""Small, transparent destination catalog. Costs are demo assumptions, not quotes."""

CATALOG = {
    "Rishikesh": {
        "tags": ["nature", "food", "wellness"], "lat": 30.0869, "lon": 78.2676,
        "source": "https://uttarakhandtourism.gov.in/destination/rishikesh",
        "return_fare": 1800, "room": 1800, "food": 650, "local": 350,
        "activities": [
            ("Ganges riverside walk", "nature", True, 0),
            ("Local vegetarian food tasting", "food", False, 350),
            ("Beginner yoga session", "wellness", False, 500),
            ("Triveni Ghat visit", "culture", True, 0),
            ("Cafe and reading break", "food", False, 250),
            ("Gentle scenic walk near town", "nature", True, 0),
        ],
    },
    "Jaipur": {
        "tags": ["culture", "food", "history"], "lat": 26.9124, "lon": 75.7873,
        "source": "https://www.tourism.rajasthan.gov.in/jaipur.html",
        "return_fare": 1600, "room": 2000, "food": 700, "local": 400,
        "activities": [
            ("Hawa Mahal exterior and old city", "history", True, 0),
            ("Rajasthani food tasting", "food", False, 400),
            ("Amber Fort visit", "history", True, 600),
            ("Local craft workshop", "culture", False, 600),
            ("Jal Mahal viewpoint", "nature", True, 0),
            ("Museum visit", "culture", False, 400),
        ],
    },
}

ASSUMPTIONS = [
    "INR estimates for the whole group; all prices are illustrative, not live fares or quotes.",
    "Delhi round-trip surface transport; outbound and return travel each reserve a day.",
    "Two adults per room, days minus one nights; food and local transport charged on every day.",
    "Activity costs are per person, additional to meals; 15% contingency included.",
    "Official tourism links support destination context, not costs, availability or opening hours.",
    "Confirm transport, opening hours, weather and accessibility before booking; no bookings made.",
]
