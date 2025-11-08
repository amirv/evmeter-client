"""Example usage of evmeter-client library."""

import asyncio
import logging
from evmeter_client import EVMeterClient, EVMeterConfig

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

async def main():
    """Example of using evmeter-client to monitor an EV charger."""
    
    # Configure with your charger details
    # Replace with your actual user ID from MQTT logs
    config = EVMeterConfig(
        user_id="EXAMPLE_USER_ID_HEX_STRING"
    )
    
    # Create client and connect
    client = EVMeterClient(config)
    print("Connecting to EV-Meter MQTT broker...")
    await client.connect()
    
    try:
        # Replace with your actual charger ID
        charger_id = "EXAMPLE123456"
        
        print(f"\n=== Getting Status for Charger {charger_id} ===")
        status = await client.get_charger_status(charger_id)
        
        print(f"Charger State: {status.charger_state}")
        print(f"EV Status: {status.ev_status}")
        print(f"Charging State: {status.charging_state}")
        print(f"Phase Type: {status.phase_type}")
        print(f"Power: {status.power_kw} kW")
        print(f"Session Energy: {status.session_energy_kwh} kWh")
        print(f"Total Energy: {status.total_energy_kwh} kWh")
        print(f"Warnings: {status.warnings}")
        print(f"Errors: {status.errors}")
        
        print(f"\n=== Getting Detailed Metrics ===")
        metrics = await client.get_charger_metrics(charger_id)
        
        print(f"Voltage L1: {metrics.voltage_l1} V")
        print(f"Voltage L2: {metrics.voltage_l2} V") 
        print(f"Voltage L3: {metrics.voltage_l3} V")
        print(f"Average Voltage: {metrics.voltage_avg} V")
        
        print(f"Current L1: {metrics.current_l1} A")
        print(f"Current L2: {metrics.current_l2} A")
        print(f"Current L3: {metrics.current_l3} A")
        print(f"Average Current: {metrics.current_avg} A")
        
        print(f"Set Current: {metrics.set_current} A")
        print(f"Circuit Breaker: {metrics.circuit_breaker} A")
        print(f"Temperature: {metrics.temperature} °C")
        
        print(f"WiFi Network: {metrics.wifi_network}")
        print(f"WiFi RSSI: {metrics.wifi_rssi} dBm")
        print(f"Firmware Version: {metrics.firmware_version}")
        print(f"Kubis Version: {metrics.kubis_version}")
        
        print(f"EVSE Status: {metrics.evse_status}")
        print(f"Ping Latency: {metrics.avg_ping_latency} ms")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        print("\nDisconnecting...")
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())