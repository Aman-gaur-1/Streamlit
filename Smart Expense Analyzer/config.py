# Prompt To Create Categories

# Generate a Python dictionary called CATEGORIES for an Indian personal finance app.
# 8 keys: Food, Travel, Shopping, Bills, Entertainment, Transfer, Healthcare, Investment.
# Values are lists of lowercase keyword strings matching Indian bank transaction descriptions.
# Include Indian apps, brands, telecom, OTT, brokers, UPI/NEFT terms.
# Output only the Python dictionary, no comments, no explanation.

CATEGORIES = {

    "Food": [
        "swiggy", "zomato", "restaurant", "bigbasket", "instamart",
        "blinkit", "dominos", "kfc", "pizza", "cafe", "haldiram",
        "food", "grocery", "bakery", "sweets", "mithai", "misthan",
        "bhandar", "dhaba", "fast food", "namkeen", "juice", "chai",
        "snack", "tiffin", "dairy", "milk", "vegetables", "fruits",
        "general store", "kirana"
    ],

    "Travel": [
        "uber", "ola", "rapido", "metro", "irctc", "petrol", "fuel",
        "airport", "bus", "railway", "cab", "auto", "parking", "toll",
        "hp pump", "indian oil", "bharat petroleum", "shell", "fuel station"
    ],

    "Shopping": [
        "amazon", "flipkart", "myntra", "ajio", "nykaa", "meesho",
        "shop", "mall", "store", "purchase", "market", "bazar",
        "bazaar", "cloth", "dress", "footwear", "shoes", "electronics"
    ],

    "Bills": [
        "electricity", "bses", "broadband", "airtel", "jio", "recharge",
        "mobile", "wifi", "internet", "dth", "gas", "water", "tata sky",
        "dish tv", "bsnl", "vodafone", "vi ", "idea", "postpaid",
        "prepaid", "cylinder", "indane", "bharat gas", "hp gas"
    ],

    "Entertainment": [
        "netflix", "spotify", "hotstar", "prime", "bookmyshow",
        "cinema", "gym", "cultfit", "disney", "youtube", "zee5"
    ],

    "Transfer": [
        "transfer", "sent to", "rent", "neft", "imps", "rtgs",
        "money sent", "paid to", "send money", "upi"
    ],

    "Healthcare": [
        "pharmacy", "hospital", "doctor", "medicine", "apollo",
        "1mg", "clinic", "medical", "diagnostic", "lab", "health",
        "netmeds", "pharmeasy", "chemist"
    ],

    "Investment": [
        "zerodha", "groww", "upstox", "mutual fund", "sip",
        "broking", "nse", "bse", "stock", "trading"
    ],
}







TAG_MAP = {
    "food":           "Food",
    "groceries":      "Food",
    "grocery":        "Food",
    "fuel":           "Travel",
    "travel":         "Travel",
    "transport":      "Travel",
    "shopping":       "Shopping",
    "miscellaneous":  "Other",
    "bill payments":  "Bills",
    "bills":          "Bills",
    "recharge":       "Bills",
    "entertainment":  "Entertainment",
    "money transfer": "Transfer",
    "transfer":       "Transfer",
    "healthcare":     "Healthcare",
    "medical":        "Healthcare",
}





CHART_LAYOUT = {
    "paper_bgcolor":    "rgba(0,0,0,0)",
    "plot_bgcolor":     "rgba(0,0,0,0)",
    "font_color":       "rgba(28,18,9,0.75)",
    "title_font_color": "rgba(28,18,9,0.85)",
    "font_family":      "DM Sans",
    "legend": {
        "font":            {"color": "rgba(28,18,9,0.80)"},
        "bgcolor":         "rgba(255,255,255,0.55)",
        "bordercolor":     "rgba(180,145,90,0.20)",
        "borderwidth":     1
    }
}



#                                                               FULL PROMPT
#
#
Create a Python file called config.py for a Smart Expense Analyzer Streamlit app targeting Indian users.

Include exactly three variables:

1. CATEGORIES — a dictionary with 8 keys: Food, Travel, Shopping, Bills, Entertainment, Transfer, Healthcare, Investment.
Each key maps to a list of lowercase keyword strings matching Indian bank transaction descriptions.
Include Indian apps, brands, UPI/NEFT terms, telecom providers, OTT platforms, fuel brands, and stock brokers.

2. TAG_MAP — a dictionary that maps common bank tag strings (like "food", "bill payments", "money transfer") to the matching CATEGORIES keys. Use lowercase keys.

3. CHART_LAYOUT — a dictionary of Plotly layout settings. Set paper_bgcolor and plot_bgcolor to transparent (rgba 0,0,0,0).
Set font_color to rgba(28,18,9,0.75), title_font_color to rgba(28,18,9,0.85), font_family to "DM Sans".
Include a legend key with font color rgba(28,18,9,0.80), bgcolor rgba(255,255,255,0.55), bordercolor rgba(180,145,90,0.20), and borderwidth 1.

Output only the Python file, no explanation outside the file.
