# Kali Safety EDR and SIEM Shield
Version: 2.0 (Collaborative Edition)
Architects: Kali Student and Gemini (AI Collaborator)

## The Mission
To Save the World through Internet Safety so others can enjoy the web without being scared of being hacked or scammed.

## Overview
This is a lightweight, proactive Endpoint Detection and Response (EDR) and SIEM tool built for Kali Linux. Unlike standard monitors that only log attacks, this shield actively intervenes to neutralize threats in real-time.

### Key Features
* Real-Time FIM: File Integrity Monitoring via watchdog to detect unauthorized file drops.
* Active Defense Kill-Switch: Automatically identifies and terminates malicious PIDs.
* Global Threat Intelligence: Synchronizes with live botnet/scammer IP feeds (Feodo Tracker).
* Persistent Protection: Runs as a systemd background service (starts at boot).
* Audit Reporting: Generates a daily_report.csv documenting every neutralized threat.

## Installation
1. Clone the repository to /home/kali/safety_monitor_test/
2. Install dependencies: sudo apt install python3-requests python3-watchdog
3. Deploy the service: sudo cp safety-edr.service /etc/systemd/system/
4. Start the shield: sudo systemctl enable --now safety-edr.service

## Collaboration Note
This project was co-authored by a Cyber Security Student and Gemini. It represents the power of Human-AI collaboration in the fight for a safer internet.
