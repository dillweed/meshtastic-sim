#!/usr/bin/env python3
"""
Meshtastic Transmission Speed Simulator

This program simulates the transmission speeds of different Meshtastic radio presets
by displaying text file contents in chunks with throttled speeds matching the
data rates of various Meshtastic configurations.
"""

import time
import sys
import os
import urllib.request
from urllib.parse import urlparse
from typing import Dict, Tuple
from datetime import datetime, timedelta

# Meshtastic radio preset configurations
# Format: (data_rate_kbps, packet_size_bytes, sf_symbols, bandwidth_khz, coding_rate, description)
RADIO_PRESETS: Dict[str, Tuple[float, int, str, int, str, str]] = {
    '1': (21.88, 237, '7/128', 500, '4/5', 'Short Range / Turbo - Fastest speed, shortest range'),
    '2': (10.94, 237, '7/128', 250, '4/5', 'Short Range / Fast - High speed, short range'),
    '3': (6.25, 237, '8/256', 250, '4/5', 'Short Range / Slow - Moderate speed, short range'),
    '4': (3.52, 237, '9/512', 250, '4/5', 'Medium Range / Fast - Good balance of speed and range'),
    '5': (1.95, 237, '10/1024', 250, '4/5', 'Medium Range / Slow - Lower speed, better range'),
    '6': (1.07, 237, '11/2048', 250, '4/5', 'Long Range / Fast - DEFAULT PRESET - Low speed, long range'),
    '7': (0.34, 237, '11/2048', 125, '4/8', 'Long Range / Moderate - Very low speed, very long range'),
    '8': (0.18, 237, '12/4096', 125, '4/8', 'Long Range / Slow - Slowest speed, maximum range'),
}

# Default sample text for testing
SAMPLE_TEXT = """Welcome to the Meshtastic Network!

This is a sample message to demonstrate transmission speeds across different radio presets. Meshtastic creates a long range, low power mesh network for communication when traditional infrastructure is unavailable.

Key features of Meshtastic:
• Long range LoRa radio communication (up to 254km record!)
• Low power consumption for battery operation
• Mesh networking with automatic message routing
• End-to-end encryption for secure communications
• GPS position sharing and tracking
• Open source hardware and software

Radio presets balance three key factors:
1. Speed - How fast data transmits
2. Range - How far signals reach
3. Reliability - How well signals penetrate obstacles

The LongFast preset is the default because it provides the best balance for most users. Faster presets like ShortTurbo are great for high-density networks, while slower presets like LongSlow maximize range for remote communications.

This simulation helps you understand how different presets affect real-world message delivery times. Try different presets to see the dramatic differences in transmission speeds!

73, and happy meshing!
"""

class MeshtasticSimulator:
    def __init__(self):
        self.default_preset = '6'  # LongFast - the Meshtastic default
        self.start_time = None
        self.total_bytes_sent = 0
        
    def display_presets(self, detailed=False):
        """Display available radio presets with optional detailed metrics"""
        print("\n" + "="*80)
        print("  MESHTASTIC RADIO PRESETS")
        print("="*80)
        
        if detailed:
            print(f"{'#':<2} {'Speed':<8} {'SF/Sym':<8} {'BW':<6} {'CR':<4} {'Range':<8} {'Description':<30}")
            print("-"*80)
            
            # Range estimates based on typical conditions
            range_estimates = {
                '1': '2-5km', '2': '3-8km', '3': '5-12km', '4': '8-15km',
                '5': '10-20km', '6': '15-25km', '7': '20-35km', '8': '25-50km+'
            }
            
            for preset_id, (speed, _, sf_symbols, bandwidth, coding_rate, description) in RADIO_PRESETS.items():
                default_marker = " ★" if preset_id == self.default_preset else "  "
                range_est = range_estimates.get(preset_id, 'Unknown')
                short_desc = description.split(' - ')[0]  # Take only the first part
                print(f"{preset_id:<2} {speed:<8.2f} {sf_symbols:<8} {bandwidth}k{'':<2} {coding_rate:<4} {range_est:<8} {short_desc}{default_marker}")
        else:
            print(f"{'#':<2} {'Speed':<8} {'Description':<50}")
            print("-"*80)
            
            for preset_id, (speed, _, _, _, _, description) in RADIO_PRESETS.items():
                default_marker = " ★" if preset_id == self.default_preset else ""
                short_desc = description.split(' - ')[0]  # Take only the first part
                print(f"{preset_id:<2} {speed:<8.2f} {short_desc}{default_marker}")
        
        print("="*80)
        if detailed:
            print("★ = Default preset  |  SF=Spreading Factor  |  BW=Bandwidth  |  CR=Coding Rate")
        else:
            print("★ = Default preset (LongFast)")
    
    def get_file_content(self, source: str) -> str:
        """Get content from file path, URL, or use sample text"""
        if source.lower() in ['sample', 'demo', 'test', 'default']:
            print("Using built-in sample text for demonstration...")
            return SAMPLE_TEXT
            
        try:
            # Check if it's a URL
            parsed = urlparse(source)
            if parsed.scheme in ('http', 'https'):
                print(f"Fetching content from URL: {source}")
                with urllib.request.urlopen(source) as response:
                    return response.read().decode('utf-8')
            else:
                # Treat as file path
                if not os.path.exists(source):
                    raise FileNotFoundError(f"File not found: {source}")
                
                print(f"Reading file: {source}")
                with open(source, 'r', encoding='utf-8') as file:
                    return file.read()
                    
        except Exception as e:
            print(f"Error reading source: {e}")
            return None
    
    def calculate_transmission_metrics(self, data_rate_kbps: float, content_length: int, packet_size: int) -> dict:
        """Calculate comprehensive transmission metrics"""
        bytes_per_second = (data_rate_kbps * 1000) / 8
        transmission_time_per_packet = packet_size / bytes_per_second
        total_packets = (content_length + packet_size - 1) // packet_size
        total_transmission_time = total_packets * transmission_time_per_packet
        effective_data_rate = (content_length / total_transmission_time) if total_transmission_time > 0 else 0
        
        return {
            'bytes_per_second': bytes_per_second,
            'transmission_time_per_packet': transmission_time_per_packet,
            'total_packets': total_packets,
            'total_transmission_time': total_transmission_time,
            'effective_data_rate_bps': effective_data_rate,
            'effective_data_rate_kbps': (effective_data_rate * 8) / 1000,
            'overhead_percentage': ((total_packets * packet_size - content_length) / content_length * 100) if content_length > 0 else 0
        }
    
    def format_time(self, seconds: float) -> str:
        """Format seconds into human readable time"""
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
        else:
            hours = seconds / 3600
            return f"{hours:.1f} hours"
    
    def display_transmission_info(self, content: str, preset_id: str):
        """Display comprehensive transmission information"""
        data_rate, packet_size, sf_symbols, bandwidth, coding_rate, description = RADIO_PRESETS[preset_id]
        metrics = self.calculate_transmission_metrics(data_rate, len(content), packet_size)
        
        print(f"\n" + "="*70)
        print(f"  TRANSMISSION ANALYSIS")
        print("="*70)
        preset_name = description.split(' - ')[0]
        print(f"Preset:     {preset_name} ({data_rate:.2f} kbps)")
        print(f"Technical:  SF {sf_symbols}, BW {bandwidth}kHz, CR {coding_rate}")
        print(f"Content:    {len(content):,} chars ({metrics['total_packets']:,} packets)")
        print(f"Duration:   {self.format_time(metrics['total_transmission_time'])}")
        print("="*70)
        
        return metrics
    
    def display_progress_bar(self, current: int, total: int, width: int = 30):
        """Display a progress bar"""
        percentage = (current / total) * 100
        filled = int(width * current // total)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {percentage:5.1f}% ({current:,}/{total:,})"
    
    def display_live_stats(self, packet_num: int, total_packets: int, bytes_sent: int, elapsed_time: float, data_rate_kbps: float):
        """Display live transmission statistics"""
        if elapsed_time > 0:
            current_rate_kbps = (bytes_sent * 8) / (elapsed_time * 1000)
            progress_bar = self.display_progress_bar(packet_num, total_packets, width=30)
            eta_seconds = (total_packets - packet_num) * (elapsed_time / packet_num) if packet_num > 0 else 0
            
            print(f"\n{progress_bar}")
            print(f"Elapsed: {self.format_time(elapsed_time)} | ETA: {self.format_time(eta_seconds)} | Rate: {current_rate_kbps:.2f} kbps")
    
    def simulate_transmission(self, content: str, preset_id: str, show_live_stats: bool = True):
        """Simulate packet transmission with specified preset"""
        if preset_id not in RADIO_PRESETS:
            print(f"Invalid preset ID: {preset_id}")
            return
        
        data_rate, packet_size, sf_symbols, bandwidth, coding_rate, description = RADIO_PRESETS[preset_id]
        metrics = self.display_transmission_info(content, preset_id)
        delay = metrics['transmission_time_per_packet']
        
        # Ask for confirmation if transmission will be very slow
        if delay > 10:
            response = input(f"\nThis will take {self.format_time(metrics['total_transmission_time'])} - very slow! Continue? (y/N): ")
            if response.lower() != 'y':
                print("Cancelled.")
                return
        elif delay > 3:
            response = input(f"\nEstimated time: {self.format_time(metrics['total_transmission_time'])}. Continue? (Y/n): ")
            if response.lower() == 'n':
                print("Cancelled.")
                return
        
        print(f"\nStarting transmission... (Press Ctrl+C to stop)")
        if delay > 1:
            print("Each dot = 1 second of transmission time\n")
        
        try:
            self.start_time = time.time()
            self.total_bytes_sent = 0
            packet_num = 1
            total_packets = metrics['total_packets']
            
            for i in range(0, len(content), packet_size):
                chunk = content[i:i + packet_size]
                
                # Display packet header - more compact
                print(f"[{packet_num:4}/{total_packets}] ", end="", flush=True)
                
                # Simulate transmission delay with visual progress
                dots_to_show = min(int(delay), 15)  # Fewer dots for cleaner look
                dot_interval = delay / dots_to_show if dots_to_show > 0 else delay
                
                for j in range(dots_to_show):
                    print(".", end="", flush=True)
                    time.sleep(dot_interval)
                
                # Handle any remaining fractional delay
                remaining_delay = delay - (dots_to_show * dot_interval)
                if remaining_delay > 0:
                    time.sleep(remaining_delay)
                
                print(" OK")
                
                # Display the actual content - cleaner formatting
                print(chunk, end="")
                
                # Update counters
                self.total_bytes_sent += len(chunk)
                elapsed_time = time.time() - self.start_time
                
                # Show live stats less frequently for cleaner output
                if show_live_stats and packet_num % max(25, total_packets // 10) == 0 and packet_num < total_packets:
                    self.display_live_stats(packet_num, total_packets, self.total_bytes_sent, elapsed_time, data_rate)
                
                packet_num += 1
                
                # Smaller pause
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            elapsed_time = time.time() - self.start_time if self.start_time else 0
            print(f"\n\nTransmission stopped after {self.format_time(elapsed_time)}")
            print(f"Sent {packet_num - 1:,} of {total_packets:,} packets ({self.total_bytes_sent:,} bytes)")
            return
        
        # Final statistics
        final_elapsed = time.time() - self.start_time
        actual_rate_kbps = (self.total_bytes_sent * 8) / (final_elapsed * 1000) if final_elapsed > 0 else 0
        
        print(f"\nTransmission complete!")
        print(f"Time: {self.format_time(final_elapsed)} | Packets: {packet_num - 1:,} | Rate: {actual_rate_kbps:.2f} kbps")
    
    def run(self):
        """Main program loop"""
        print("MESHTASTIC TRANSMISSION SIMULATOR")
        print("Default: LongFast (#6)")
        
        while True:
            print(f"\n" + "="*50)
            print("1. View radio presets")
            print("2. View detailed specs")
            print("3. Simulate transmission")
            print("4. Quick demo")
            print("5. Exit")
            print("="*50)
            
            choice = input("Option (1-5): ").strip()
            
            if choice == '1':
                self.display_presets(detailed=False)
                
            elif choice == '2':
                self.display_presets(detailed=True)
                
            elif choice == '3':
                print(f"\nFile source:")
                print("• File path: /path/to/file.txt")
                print("• URL: https://example.com/text.txt")
                print("• 'sample' for demo text")
                
                source = input("\nSource: ").strip()
                if not source:
                    print("No source provided.")
                    continue
                
                # Get file content
                content = self.get_file_content(source)
                if content is None:
                    continue
                
                if not content.strip():
                    print("File is empty.")
                    continue
                
                # Display presets and get selection
                self.display_presets(detailed=False)
                preset_input = input(f"\nPreset (1-8, Enter for #{self.default_preset}): ").strip()
                preset_id = preset_input if preset_input else self.default_preset
                
                # Start simulation
                self.simulate_transmission(content, preset_id)
                
            elif choice == '4':
                # Quick demo
                print(f"\nQuick demo with LongFast preset...")
                self.simulate_transmission(SAMPLE_TEXT, self.default_preset, show_live_stats=False)
                
            elif choice == '5':
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice.")

def main():
    """Entry point"""
    simulator = MeshtasticSimulator()
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if len(sys.argv) >= 2:
            source = sys.argv[1]
            preset_id = sys.argv[2] if len(sys.argv) > 2 else simulator.default_preset
            
            print(f"Direct mode: {source} with preset #{preset_id}")
            content = simulator.get_file_content(source)
            if content is not None:
                simulator.simulate_transmission(content, preset_id)
        else:
            print("Usage: python meshtastic_sim.py [file_or_url] [preset_id]")
            print(f"Default preset: {simulator.default_preset} (LongFast)")
    else:
        # Interactive mode
        try:
            simulator.run()
        except KeyboardInterrupt:
            print("\nGoodbye!")

if __name__ == "__main__":
    main()