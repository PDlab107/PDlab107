# PDlab Denture Repair - Complete Setup Guide

This guide will walk you through setting up your Shopify website for the denture repair service.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Shopify Account Setup](#shopify-account-setup)
3. [Theme Installation](#theme-installation)
4. [Page Creation](#page-creation)
5. [Navigation Setup](#navigation-setup)
6. [Theme Customization](#theme-customization)
7. [Content Creation](#content-creation)
8. [SEO Configuration](#seo-configuration)
9. [Testing](#testing)
10. [Go Live](#go-live)

---

## Prerequisites

Before you begin, you'll need:
- ✅ A Shopify account (sign up at shopify.com)
- ✅ This theme package (all files from the repository)
- ✅ Your business information (address, phone, email)
- ✅ Logo image (recommended: 200x50px PNG with transparent background)
- ✅ Business photos (team, workshop, before/after denture repairs)
- ✅ Payment gateway account (Shopify Payments or alternative)

---

## Shopify Account Setup

### Step 1: Create Your Shopify Store

1. Go to [shopify.com](https://www.shopify.com)
2. Click "Start free trial"
3. Enter your email address
4. Follow the setup wizard:
   - Store name: "PDlab Denture Repair" (or your business name)
   - What will you sell: "Services"
   - Where will you sell: "United Kingdom"

### Step 2: Choose a Plan

After the trial:
- **Recommended**: Basic Shopify (£24/month) - Sufficient for most needs
- **Alternative**: Shopify (£69/month) - If you need advanced reports

### Step 3: Set Up Your Domain

1. In Shopify Admin, go to: **Settings > Domains**
2. Options:
   - **Buy new domain**: Purchase through Shopify
   - **Connect existing domain**: If you already own pdlab.co.uk
3. Follow the instructions to connect your domain

---

## Theme Installation

### Method 1: Manual Upload (Recommended for Beginners)

1. **Create a ZIP file**:
   ```bash
   # On Mac/Linux, run in terminal:
   cd /path/to/theme/folder
   zip -r pdlab-theme.zip assets config layout locales sections snippets templates
   
   # On Windows, select all folders and right-click > Send to > Compressed folder
   ```

2. **Upload to Shopify**:
   - In Shopify Admin, go to: **Online Store > Themes**
   - Click "Add theme" button
   - Select "Upload zip file"
   - Choose your pdlab-theme.zip
   - Wait for upload to complete

3. **Activate Theme**:
   - Find "PDlab Denture Repair" in the theme library
   - Click "Actions" > "Publish"

### Method 2: Using Shopify CLI (For Developers)

1. **Install Shopify CLI**:
   ```bash
   npm install -g @shopify/cli @shopify/theme
   ```

2. **Login to Your Store**:
   ```bash
   shopify login --store your-store.myshopify.com
   ```

3. **Push Theme**:
   ```bash
   cd /path/to/theme/folder
   shopify theme push
   ```

---

## Page Creation

You need to create 8 main pages in Shopify Admin.

### Step-by-Step for Each Page:

1. Go to: **Online Store > Pages**
2. Click "Add page"
3. For each page below, enter the information and assign the template:

#### Page 1: About Us
- **Title**: About Us
- **Content**: (Leave blank - template handles content)
- **Template**: `page.about`
- **Visibility**: Visible
- **Search engine listing**: 
  - Title: "About PDlab Denture Repair - Expert Technicians"
  - Description: "Learn about our team, certifications, and commitment to quality denture repair services."

#### Page 2: How It Works
- **Title**: How It Works
- **Template**: `page.how-it-works`
- **Search engine listing**:
  - Title: "How Our Denture Repair Service Works - Simple 4-Step Process"
  - Description: "Learn how to send your dentures for professional repair. Fast, secure, and fully insured postal service."

#### Page 3: Services
- **Title**: Services
- **Template**: `page.services`
- **Search engine listing**:
  - Title: "Denture Repair Services - Cracks, Teeth, Reline, Cleaning"
  - Description: "Professional acrylic denture repair services. Cracked denture repair, tooth replacement, reline, cleaning, and adjustments."

#### Page 4: Pricing
- **Title**: Pricing
- **Template**: `page.pricing`
- **Search engine listing**:
  - Title: "Transparent Denture Repair Pricing - From £35"
  - Description: "Clear pricing for denture repair services. No hidden costs. Basic repair from £50, tooth replacement from £65."

#### Page 5: Contact
- **Title**: Contact
- **Template**: `page.contact`
- **Search engine listing**:
  - Title: "Contact PDlab Denture Repair - Phone, Email, WhatsApp"
  - Description: "Get in touch with our denture repair experts. Phone, email, WhatsApp, and contact form available."

#### Page 6: Privacy Policy
- **Title**: Privacy Policy
- **Template**: `page.privacy-policy`

#### Page 7: Refund Policy
- **Title**: Refund Policy
- **Template**: `page.refund-policy`

#### Page 8: Shipping Policy
- **Title**: Shipping Policy
- **Template**: `page.shipping-policy`

---

## Navigation Setup

### Main Menu

1. Go to: **Online Store > Navigation**
2. Click on "Main menu"
3. Remove default items and add these links:
   - Home → /
   - About Us → /pages/about
   - How It Works → /pages/how-it-works
   - Services → /pages/services
   - Pricing → /pages/pricing
   - Blog → /blogs/denture-care
   - Contact → /pages/contact

### Footer Menu

1. In Navigation, click "Footer menu" (or create it)
2. Add these links:
   - Privacy Policy → /pages/privacy-policy
   - Refund Policy → /pages/refund-policy
   - Shipping Policy → /pages/shipping-policy
   - Terms of Service → /pages/terms-of-service (if you create this page)

---

## Theme Customization

### Access Theme Editor

Go to: **Online Store > Themes > Customize**

### 1. Logo Upload

1. In theme editor sidebar, find "Logo" section
2. Click "Select image" or "Upload"
3. Upload your logo (200x50px recommended)
4. Adjust logo width slider if needed

### 2. Contact Information

Fill in all contact details:
- **Phone**: +44 123 456 7890 (your actual number)
- **Email**: info@pdlab.co.uk (your actual email)
- **Address**: Your complete business address
- **WhatsApp**: 441234567890 (your number without + or spaces)
- **Business Hours**: Your actual hours

### 3. Colors (Optional)

Default colors are optimized for readability, but you can customize:
- **Primary Color**: #2563eb (blue)
- **Secondary Color**: #10b981 (green)
- **Text Color**: #1f2937 (dark gray)
- **Background**: #ffffff (white)

### 4. Typography

- **Font Size**: Keep at 18px (senior-friendly) or increase to 20-22px
- **Font Family**: Inter (default) is highly readable

### 5. Trust Badges

Customize the 4 trust badge texts if needed:
1. Fast Turnaround
2. Money-Back Guarantee
3. Fully Insured Postage
4. Expert Technicians

### 6. Homepage Hero Section

- **Hero Title**: Customize your main headline
- **Hero Subtitle**: Customize your subheadline
- **Button Text**: Default is "Repair My Dentures"
- **Button Link**: Should point to /pages/services

### 7. SEO Settings

- **Meta Title**: Add homepage title
- **Meta Description**: Customize homepage description
- **Meta Keywords**: Add relevant keywords
- **Social Image**: Upload 1200x630px image for social sharing

### 8. Favicon

1. Go to: **Settings > General**
2. Scroll to "Favicon"
3. Upload a square image (32x32px minimum, 512x512px recommended)

---

## Content Creation

### 1. Create Blog

1. Go to: **Online Store > Blog posts > Manage blogs**
2. Click "Add blog"
3. Name it: "Denture Care"
4. Handle: denture-care (auto-generated)
5. Save

### 2. Write Blog Posts

Create at least 3-5 initial blog posts:

**Post 1: How to Take Care of Your Dentures**
- Tips for daily cleaning
- Storage recommendations
- What to avoid
- When to seek professional help

**Post 2: Everything You Need to Know About Denture Repairs**
- Common denture problems
- Types of repairs available
- When to repair vs. replace
- How the repair process works

**Post 3: Signs It's Time to Replace Your Dentures**
- Wear and tear indicators
- Fit problems
- Age of dentures
- Professional assessment

**Post 4: How to Ship Your Dentures Safely**
- Packaging materials needed
- Step-by-step instructions
- Insurance and tracking
- What to include in the package

**Post 5: Common Denture Problems and Solutions**
- Loose dentures
- Cracks and breaks
- Staining
- Sore spots
- Solutions for each

### 3. Add Images

For each page and blog post, add relevant images:
- **About page**: Team photos, laboratory photos
- **Services page**: Before/after repair photos
- **Blog posts**: Relevant illustrations or photos

Image specifications:
- Format: JPG or PNG
- Homepage hero: 1920x1080px
- Service images: 800x600px
- Blog featured images: 1200x630px
- Optimize all images (use TinyPNG.com or similar)

### 4. Testimonials

Add 5-10 customer testimonials:
1. Real customer names (first name + initial)
2. Location (city)
3. 5-star ratings
4. Genuine feedback about service

Place in:
- Homepage testimonials section (edit index.liquid if needed)
- Create a dedicated testimonials page (optional)

---

## SEO Configuration

### 1. Google Search Console

1. Go to [search.google.com/search-console](https://search.google.com/search-console)
2. Add your website property
3. Verify ownership (follow Google's instructions)
4. Submit sitemap: yoursite.com/sitemap.xml

### 2. Google Business Profile

1. Go to [google.com/business](https://www.google.com/business)
2. Create or claim your business listing
3. Add:
   - Business name
   - Address
   - Phone
   - Hours
   - Photos
   - Service area
   - Description

### 3. Meta Tags

Already included in the theme! The theme automatically generates:
- Meta descriptions
- Schema.org markup
- Open Graph tags
- Twitter Cards

### 4. Keywords to Target

Primary:
- denture repair
- denture repair by post
- acrylic denture repair
- denture repair UK

Secondary:
- broken denture repair
- cracked denture repair
- tooth replacement dentures
- denture services

Long-tail:
- how to repair broken dentures
- denture repair service near me
- postal denture repair UK
- emergency denture repair

### 5. Local SEO

- Ensure business address is consistent everywhere
- Get listed in UK business directories
- Encourage customer reviews on Google
- Create location-specific content if serving specific areas

---

## Testing

### 1. Functionality Testing

Test these features:
- ✅ All navigation links work
- ✅ Contact form submits correctly
- ✅ Phone/email links work on mobile
- ✅ Image upload in services page works
- ✅ FAQ accordions expand/collapse
- ✅ Mobile menu toggles
- ✅ All pages load correctly

### 2. Mobile Testing

Test on actual mobile devices:
- ✅ iPhone (Safari)
- ✅ Android (Chrome)
- ✅ Tablet (iPad)

Check:
- Text is readable (not too small)
- Buttons are easy to tap
- Forms work correctly
- Images display properly
- Navigation is usable

### 3. Browser Testing

Test in these browsers:
- ✅ Chrome
- ✅ Firefox
- ✅ Safari
- ✅ Edge

### 4. Accessibility Testing

- ✅ Use keyboard to navigate (Tab key)
- ✅ Test with screen reader (if possible)
- ✅ Check color contrast (use WebAIM contrast checker)
- ✅ Ensure all images have alt text

### 5. Performance Testing

Use Google PageSpeed Insights:
1. Go to [pagespeed.web.dev](https://pagespeed.web.dev)
2. Enter your URL
3. Aim for:
   - Mobile score: 80+
   - Desktop score: 90+

Optimize if needed:
- Compress images
- Enable Shopify's image optimization
- Minimize apps/plugins

---

## Go Live

### Pre-Launch Checklist

- [ ] All pages created and tested
- [ ] Contact information updated
- [ ] Logo uploaded
- [ ] Navigation menus configured
- [ ] At least 3 blog posts published
- [ ] Contact form tested
- [ ] Payment gateway configured
- [ ] Shipping/refund policies reviewed
- [ ] Domain connected
- [ ] Favicon uploaded
- [ ] Google Analytics added (optional)
- [ ] SSL certificate active (Shopify provides this)

### Launch Steps

1. **Remove Password Protection**:
   - Go to: **Online Store > Preferences**
   - Uncheck "Restrict access with password"
   - Save

2. **Announce Launch**:
   - Email existing customers
   - Post on social media
   - Update Google Business Profile
   - Add website to business cards/materials

3. **Monitor**:
   - Check Google Analytics daily
   - Monitor contact form submissions
   - Respond to inquiries promptly
   - Track any errors or issues

---

## Post-Launch Maintenance

### Weekly Tasks
- Check and respond to contact form messages
- Monitor order inquiries
- Review website performance

### Monthly Tasks
- Publish new blog post
- Update testimonials
- Review and update pricing if needed
- Check for broken links
- Review analytics data

### Quarterly Tasks
- Update images and photos
- Refresh homepage content
- Review and update SEO keywords
- Backup website data
- Review and respond to customer feedback

---

## Support Resources

### Shopify Help Center
- [help.shopify.com](https://help.shopify.com)

### Shopify Community
- [community.shopify.com](https://community.shopify.com)

### Theme Documentation
- Included in README.md file

### Contact for Theme Support
- Email: info@pdlab.co.uk
- Phone: +44 123 456 7890

---

## Troubleshooting

### Problem: Theme not appearing after upload
**Solution**: Ensure ZIP file only contains theme folders (assets, config, layout, locales, sections, snippets, templates). Don't include parent folder.

### Problem: Pages showing "Template not found"
**Solution**: When creating pages, make sure to select the correct template from dropdown (e.g., page.about, page.services).

### Problem: Navigation links not working
**Solution**: Ensure page URLs are correct. Use /pages/page-name format.

### Problem: Contact form not working
**Solution**: Check Shopify notification settings. Go to: Settings > Notifications > Customer notifications.

### Problem: Images not loading
**Solution**: Ensure images are uploaded to Shopify. Use Shopify's file manager: Settings > Files.

### Problem: Mobile menu not working
**Solution**: Clear browser cache and test again. Ensure JavaScript is not blocked.

---

## Conclusion

Congratulations! Your PDlab Denture Repair website should now be live and ready to accept customer inquiries.

Remember:
- Keep content fresh with regular blog posts
- Respond promptly to inquiries
- Monitor and improve based on customer feedback
- Update pricing and services as your business grows

For additional help, refer to the README.md file or contact Shopify support.

Good luck with your denture repair business! 🦷✨
