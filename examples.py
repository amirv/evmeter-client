#!/usr/bin/env python3
"""
EV-Meter Client Examples

This script demonstrates various ways to use the evmeter-client library:
1. Basic charger status monitoring
2. Raw MQTT message monitoring
3. Parsing BLEWIFI protocol messages
"""

import asyncio
import logging
from datetime import datetime

from evmeter_client import EVMeterClient, EVMeterConfig
from evmeter_client.parser import parse_blewifi_payload

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def basic_monitoring_example():
    """Example 1: Basic charger status monitoring"""
    print("=== Basic Charger Monitoring ===")
    
    config = EVMeterConfig(
        user_id="your-hex-user-id-here"  # Replace with your actual user ID
    )
    
    client = EVMeterClient(config)
    
    try:
        await client.connect()
        print("✓ Connected to EV-Meter MQTT broker")
        
        # Replace with your actual charger ID
        charger_id = "0434335121105646"  
        
        # Get current status
        try:
            status = await client.get_charger_status(charger_id)
            print(f"Charger State: {status.charger_state}")
            print(f"EV Status: {status.ev_status}")
            print(f"Power: {status.power_kw} kW")
            print(f"Session Energy: {status.session_energy_kwh} kWh")
            
            # Get detailed metrics
            metrics = await client.get_charger_metrics(charger_id)
            print(f"Voltage L1: {metrics.voltage_l1} V")
            print(f"Current L1: {metrics.current_l1} A")
            
        except Exception as e:
            print(f"Error getting charger data: {e}")
            print("Note: Make sure to replace the user_id and charger_id with your actual values")
            
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        await client.disconnect()


async def mqtt_monitoring_example():
    """Example 2: Raw MQTT message monitoring (similar to the CLI tool)"""
    print("\\n=== MQTT Message Monitoring ===")
    print("This will monitor MQTT messages for 10 seconds...")
    
    import aiomqtt
    
    try:
        async with aiomqtt.Client(
            hostname="iot.nayax.com",
            port=1883,
            username="deviceEV",
            password="ng4GycjMmuvpSJU6",
        ) as client:
            await client.subscribe("#")
            print("✓ Subscribed to all MQTT topics")
            
            message_count = 0
            start_time = datetime.now()
            
            async for message in client.messages:
                # Stop after 10 seconds or 10 messages
                if (datetime.now() - start_time).seconds > 10 or message_count >= 10:
                    break
                    
                message_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                topic = message.topic.value
                payload = message.payload
                
                print(f"[{timestamp}] {topic}: {payload}")
                
                # Try to parse if it looks like BLEWIFI data
                try:
                    if payload and len(payload) > 4:
                        parsed = parse_blewifi_payload(payload)
                        print(f"  → Parsed: {parsed}")
                except:
                    pass  # Ignore parsing failures for this example
                    
            print(f"Monitored {message_count} messages")
            
    except Exception as e:
        print(f"MQTT monitoring error: {e}")


def parsing_example():
    """Example 3: Parsing raw BLEWIFI messages"""
    print("\\n=== BLEWIFI Protocol Parsing ===")
    
    # Example hex data (this would come from MQTT in practice)
    sample_hex_data = bytes.fromhex("aa5517000102030405060708090a0b0c0d0e0f101112131415")
    
    try:
        parsed_data = parse_blewifi_payload(sample_hex_data)
        print("✓ Successfully parsed BLEWIFI message:")
        for key, value in parsed_data.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"✗ Parsing failed: {e}")
        print("Note: This is expected with sample data - real BLEWIFI messages are needed")


async def main():
    """Run all examples"""
    print("EV-Meter Client Examples")
    print("=" * 50)
    
    # Run examples
    await basic_monitoring_example()
    await mqtt_monitoring_example()
    parsing_example()
    
    print("\\n" + "=" * 50)
    print("Examples completed!")
    print("\\nFor continuous monitoring, use:")
    print("  evmeter-monitor                    # CLI tool")
    print("  python mqtt_monitor.py             # Standalone script")


if __name__ == "__main__":
    asyncio.run(main())