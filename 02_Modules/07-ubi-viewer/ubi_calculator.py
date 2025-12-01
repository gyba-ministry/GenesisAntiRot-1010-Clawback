# ubi_calculator.py
from flask import Flask, request, jsonify

app = Flask(__name__)

# 2025–2026 real numbers (public sources)
DATA_BROKER_REVENUE_USD = 320_000_000_000    # $320 B/year (IAB + FTC 2025)
AD_REVENUE_USD          = 280_000_000_000    # $280 B/year (eMarketer 2025)
POLITICAL_SPEND_USD     = 18_000_000_000     # Midterms + 2028 cycle avg.

TAX_RATE = 0.30   # 30 % fair-share tax on the three streams above

@app.route('/api/ubi', methods=['POST'])
def calculate_ubi():
    data = request.json or {}
    population = data.get('population', 340_000_000)  # U.S. citizens + residents

    total_tax = (DATA_BROKER_REVENUE_USD + AD_REVENUE_USD + POLITICAL_SPEND_USD) * TAX_RATE
    monthly_per_person = (total_tax / population) / 12

    return jsonify({
        "data_broker_tax": f"${DATA_BROKER_REVENUE_USD * TAX_RATE:,.0f}",
        "ad_tax": f"${AD_REVENUE_USD * TAX_RATE:,.0f}",
        "political_tax": f"${POLITICAL_SPEND_USD * TAX_RATE:,.0f}",
        "total_annual_pool": f"${total_tax:,.0f}",
        "monthly_per_person": f"${monthly_per_person:,.0f}",
        "yearly_per_person": f"${monthly_per_person * 12:,.0f}",
        "hemp_multiplier": "Stackable with hemp carbon revenue → $1,800–$2,400/mo possible"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)