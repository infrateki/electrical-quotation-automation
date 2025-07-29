"""Integration test to demonstrate the ProQuote system working end-to-end."""

import asyncio
import httpx
import json
from datetime import datetime


async def test_proquote_system():
    """Test the complete ProQuote quotation generation flow."""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("🚀 ProQuote Integration Test")
        print("=" * 50)
        
        # 1. Check health
        print("\n1️⃣ Checking API health...")
        health_response = await client.get(f"{base_url}/api/v1/health")
        print(f"   Health Status: {health_response.json()['status']}")
        
        # 2. Create a new quotation
        print("\n2️⃣ Creating new quotation...")
        quotation_data = {
            "company_name": "ProQuote Electrical Services",
            "prepared_by": "John Smith",
            "client_name": "ABC Corporation",
            "client_contact": "jane.doe@abc.com",
            "project_name": "Office Renovation - Building A",
            "validity_days": 45
        }
        
        create_response = await client.post(
            f"{base_url}/api/v1/quotations",
            json=quotation_data
        )
        quotation = create_response.json()
        quotation_id = quotation["id"]
        print(f"   Created Quotation ID: {quotation_id}")
        print(f"   Quote Number: {quotation['quote_number']}")
        
        # 3. Trigger quotation generation
        print("\n3️⃣ Triggering quotation generation with AI agents...")
        generate_response = await client.post(
            f"{base_url}/api/v1/quotations/{quotation_id}/generate"
        )
        print(f"   Status: {generate_response.json()['status']}")
        
        # 4. Wait and check status
        print("\n4️⃣ Checking generation status...")
        await asyncio.sleep(2)  # Give agents time to process
        
        status_response = await client.get(
            f"{base_url}/api/v1/quotations/{quotation_id}/status"
        )
        status_data = status_response.json()
        
        print(f"   Generation Status: {status_data['status']}")
        
        if status_data['status'] == 'generated' and 'generated_data' in status_data:
            generated = status_data['generated_data']
            
            print("\n✅ Quotation Generated Successfully!")
            print("\n📄 Generated Data:")
            print(f"   - Quote Number: {generated.get('quote_number')}")
            print(f"   - Company: {generated.get('company_info', {}).get('name')}")
            
            if generated.get('header'):
                print("\n   Header Section:")
                print(f"     - Status: {generated['header'].get('status')}")
                print(f"     - Valid Until: {generated['header'].get('valid_until')}")
            
            if generated.get('footer'):
                print("\n   Footer Section:")
                print(f"     - Terms: {'✓' if generated['footer'].get('terms_and_conditions') else '✗'}")
                print(f"     - Disclaimer: {'✓' if generated['footer'].get('disclaimer') else '✗'}")
            
            print("\n   Agent Execution Log:")
            for log in generated.get('agent_logs', []):
                print(f"     - {log['agent_name']}: {log['status']} ({log['execution_time_ms']}ms)")
        
        elif status_data['status'] == 'failed':
            print(f"\n❌ Generation Failed: {status_data.get('error')}")
        
        # 5. List all quotations
        print("\n5️⃣ Listing all quotations...")
        list_response = await client.get(f"{base_url}/api/v1/quotations")
        quotations = list_response.json()
        print(f"   Total Quotations: {len(quotations)}")
        
        for q in quotations:
            print(f"   - {q['quote_number']} | {q['client_name']} | Status: {q['status']}")
        
        # 6. Check agent status
        print("\n6️⃣ Checking agent status...")
        agents_response = await client.get(f"{base_url}/api/v1/agents")
        agents = agents_response.json()
        
        print("   Agent Registry:")
        for agent in agents:
            print(f"   - {agent['name']}: {agent['status']} ({agent['type']}) - {agent['tasks_completed']} tasks")
        
        print("\n" + "=" * 50)
        print("✨ Integration test completed!")


if __name__ == "__main__":
    print("Starting ProQuote Integration Test...")
    print("Make sure the API is running: uvicorn api.main:app --reload")
    print("")
    
    asyncio.run(test_proquote_system())