# UK Vehicle Parts Checker

A mobile-first web app for checking whether a part number or OEM code is compatible with a UK-registered vehicle.

## Features

- 🔍 Look up any UK vehicle by registration number (using the DVLA VES API)
- 🔩 Enter a part number or OEM code to identify the brand and type
- ✅ Instant compatibility assessment based on vehicle make and part brand
- 🔗 One-tap links to search GSF Car Parts, Euro Car Parts, Autodoc, and eBay UK
- 📋 History of recent checks
- 📱 Designed for iPhone (home screen installable)

## Setup

### 1. Get a Free DVLA API Key

The app uses the official DVLA Vehicle Enquiry Service (VES) API, which is **free**.

1. Go to: https://developer-portal.driver-vehicle-licensing.api.gov.uk/
2. Register and create an application
3. Subscribe to the **Vehicle Enquiry Service** API (free tier)
4. Copy your API key

### 2. Open the App on Your iPhone

**Option A – GitHub Pages (recommended)**

1. Push this repository to GitHub
2. Enable GitHub Pages on the `vehicle-parts-checker/` folder (or root)
3. Open the URL in Safari on your iPhone
4. Tap **Share → Add to Home Screen** to install it as an app

**Option B – Open directly**

Open `vehicle-parts-checker/index.html` in any browser.

### 3. Enter Your API Key

Tap the ⚙️ icon in the top-right corner and paste your DVLA API key. It is stored locally on your device and never sent anywhere except the official DVLA API endpoint.

## How It Works

1. Enter a full UK registration number (e.g. `AB12 CDE`)
2. Enter a part number or OEM code (e.g. `1J0407271E` or `NGK BKUR6ET-10`)
3. Tap **Check Compatibility**

The app will:
- Fetch the vehicle's make, model, year, fuel type, and engine size from DVLA
- Identify the part manufacturer from the OEM code prefix
- Assess compatibility based on whether the part brand matches the vehicle group
- Provide direct search links to verify fitment

## Compatibility Logic

| Result | Meaning |
|--------|---------|
| ✅ Likely Compatible | The OEM brand matches the vehicle manufacturer group |
| ❌ Likely Incompatible | The part appears to be genuine OEM for a different brand |
| 🔍 Verify Fitment | Aftermarket part — likely compatible but confirm via retailer |

> **Note:** This app provides a first-pass compatibility check. Always confirm fitment using a parts retailer's vehicle lookup tool before ordering.

## Supported OEM Prefixes

The app recognises parts from: VW Group (Audi, VW, SEAT, Skoda, Porsche), BMW / MINI, Mercedes-Benz, Ford, Vauxhall/Opel, Fiat/Alfa/Jeep, Land Rover/Jaguar, NGK, LUK, INA, FAG, SKF, TRW, Delphi, Bosch, Blueprint, FEBI, Mahle, Mann-Filter, Moog, Sachs, Hella, Mintex, Corteco, ATE, WIX, and more.
