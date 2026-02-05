# E-Commerce Setup Guide

This guide will help you set up your Shopify products for the new e-commerce functionality.

## Overview

The website has been converted from a quote-based system to a full e-commerce checkout experience. Customers can now add services directly to their cart and checkout securely through Shopify.

## What Changed

### 1. Homepage
- ✅ Fixed button formatting - both "Repair My Dentures" and "How It Works" buttons now have consistent styling

### 2. Services Page
- ✅ Now displays products from a Shopify collection named "services"
- ✅ Each service has an "Add to Cart" button instead of "Get a Free Quote"
- ✅ Customers can add special instructions for each service
- ✅ Fallback to static content with instructions if products aren't set up yet

### 3. Cart Integration
- ✅ AJAX cart functionality - items are added without page reload
- ✅ Visual feedback when items are added (green notification)
- ✅ Cart icon in header shows item count
- ✅ Cart badge updates automatically

## How to Set Up Products

### Step 1: Create a Collection

1. In your Shopify admin, go to **Products** → **Collections**
2. Click **Create collection**
3. Set the collection handle to: `services` (this is important!)
4. Set the title to: "Denture Repair Services" or similar
5. Save the collection

### Step 2: Create Products

Create the following 5 products and add them to the "services" collection:

#### Product 1: Cracked Denture Repair
- **Title:** Cracked Denture Repair
- **Price:** £50.00 (or higher based on complexity)
- **Description:**
  ```
  Has your denture cracked or broken? Our expert technicians specialize in repairing cracks, breaks, and fractures in acrylic dentures.
  
  What's included:
  • Professional structural repair using high-quality bonding materials
  • Reinforcement to prevent future cracks
  • Professional cleaning and sanitizing
  • Polishing for a natural finish
  • Quality inspection before return
  ```
- **Collection:** services
- **Optional:** Add product variants if you offer different repair levels (Basic, Standard, Premium)

#### Product 2: Tooth Replacement
- **Title:** Tooth Replacement
- **Price:** £65.00 per tooth
- **Description:**
  ```
  Missing or broken teeth on your dentures? We can replace individual teeth or multiple teeth, ensuring they match perfectly with your existing dentures.
  
  What's included:
  • Replacement of broken or missing teeth
  • Perfect color and size matching
  • Secure bonding for long-lasting results
  • Professional polishing and finishing
  • Complete sanitization
  ```
- **Collection:** services
- **Optional:** Add variants for number of teeth (1 tooth, 2 teeth, 3+ teeth)

#### Product 3: Denture Reline
- **Title:** Denture Reline
- **Price:** £80.00
- **Description:**
  ```
  Over time, your gums and bone structure can change, causing dentures to become loose or uncomfortable. A professional reline restores the fit for maximum comfort.
  
  What's included:
  • Complete reline of denture base
  • Improved fit and comfort
  • Better stability and retention
  • Professional cleaning and polishing
  • Reduced movement while eating and speaking
  ```
- **Collection:** services

#### Product 4: Professional Cleaning & Polishing
- **Title:** Professional Cleaning & Polishing
- **Price:** £35.00
- **Description:**
  ```
  Even with regular home cleaning, dentures can develop stains, tartar, and discoloration. Our professional cleaning service restores their appearance.
  
  What's included:
  • Deep professional cleaning
  • Stain removal
  • Tartar and plaque removal
  • High-gloss polishing
  • Complete sanitization
  ```
- **Collection:** services

#### Product 5: Denture Adjustments
- **Title:** Denture Adjustments
- **Price:** £40.00
- **Description:**
  ```
  Are your dentures causing sore spots or discomfort? We can make precise adjustments to eliminate pressure points and improve fit.
  
  What's included:
  • Precise adjustment of pressure points
  • Elimination of sore spots
  • Improved comfort during wear
  • Professional smoothing and finishing
  • Quality inspection
  ```
- **Collection:** services

### Step 3: Add Product Images (Optional)

For each product, you can add images:
- Photos of the repair process
- Before/after examples
- Your lab or technicians at work
- If no image is added, the template will show emoji placeholders

### Step 4: Test the Integration

1. Visit your services page at `/pages/services`
2. You should now see all 5 products with "Add to Cart" buttons
3. Try adding a product to cart
4. You should see a green notification: "Product added to cart!"
5. Check the cart icon in the header - it should show the item count
6. Click "View Cart & Checkout" to proceed to checkout

## Customer Instructions

When customers add services to their cart, they can:
1. Add special instructions in the textarea field on each product
2. Select variants if you've set them up (e.g., number of teeth to replace)
3. Proceed to checkout normally through Shopify
4. Instructions they entered will be attached to their order as line item properties

## Features

### Special Instructions Field
Each product has an optional "Special Instructions" field where customers can:
- Describe the damage in detail
- Mention color preferences
- Request rush service
- Add any other relevant information

### AJAX Cart
- Products are added to cart without page reload
- Visual feedback confirms successful addition
- Error handling if something goes wrong
- Cart count updates automatically

### Responsive Design
- All layouts work on mobile, tablet, and desktop
- Touch-friendly buttons for senior users
- Clear, readable text at all sizes

## Troubleshooting

### Products Not Showing?
- Make sure you created a collection with the handle `services` (not "Services" or "services-collection")
- Ensure all products are added to this collection
- The collection must be active/published

### Add to Cart Not Working?
- Check browser console for errors
- Ensure JavaScript is enabled
- Clear your browser cache
- Make sure products have available variants

### Cart Count Not Updating?
- This is controlled by JavaScript in `theme.js`
- Make sure the theme JavaScript is loading properly
- Check for JavaScript errors in browser console

## Need Help?

If you need assistance setting up your products or have questions about the new e-commerce functionality, please refer to Shopify's documentation or contact support.

## Technical Details

### Files Modified
- `templates/index.liquid` - Fixed button formatting
- `templates/page.services.liquid` - Added product integration and cart forms
- `assets/theme.js` - Added AJAX cart functionality
- `sections/header.liquid` - Added cart icon with item count

### Shopify Liquid Used
- `collections['services'].products` - Loops through products in services collection
- `product.price | money` - Formats prices in store currency
- `product.selected_or_first_available_variant.id` - Gets variant ID for cart
- `properties[Instructions]` - Captures custom cart attributes

### JavaScript Features
- Fetch API for AJAX cart adds
- Event delegation for form handling
- Visual notifications for user feedback
- Automatic cart count updates
