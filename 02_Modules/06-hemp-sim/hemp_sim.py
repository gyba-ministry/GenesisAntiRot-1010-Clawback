from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/api/hemp-sim', methods=['POST'])
def hemp_simulator():
    data = request.json
    acres = data.get('acres', 1)
    data_sales_rate = data.get('data_sales_rate', 0.05)
    ad_rate = data.get('ad_rate', 0.10)
    political_spend_rate = data.get('political_spend_rate', 0.15)
    
    biofuel_gal = acres * 300  # gal/year
    carbon_credits = acres * 3000  # $3K/acre
    co2_cut = acres * 10  # tons/year
    total_revenue = carbon_credits + (biofuel_gal * 5)  # $5/gal market
    ubi_data = total_revenue * data_sales_rate
    ubi_ads = total_revenue * ad_rate
    ubi_political = total_revenue * political_spend_rate
    total_ubi = ubi_data + ubi_ads + ubi_political

    
    
    result = {
        'acres': acres,
        'biofuel_gal': biofuel_gal,
        'carbon_credits': f"${carbon_credits}",
        'co2_cut': f"{co2_cut} tons (SDG 13 aligned)",
        'total_revenue': f"${total_revenue}",
        'ubi_from_data': f"${ubi_data}",
        'ubi_from_ads': f"${ubi_ads}",
        'ubi_from_political': f"${ubi_political}",
        'total_ubi_per_user': f"${total_ubi / 1000:.2f} (per 1K users)",
        'dod_impact': f"Reduces AI power load 70% – secures $50B JWCC"
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
