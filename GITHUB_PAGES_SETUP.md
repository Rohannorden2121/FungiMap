# GitHub Pages Setup Instructions for FungiMap

## ✅ Your Landing Page is Ready!

I've created a professional landing page for FungiMap using your exact text. Here's what to do next:

---

## 🚀 Step 1: Enable GitHub Pages

1. Go to your repository on GitHub: https://github.com/Rohannorden2121/FungiMap

2. Click on **Settings** (top menu)

3. In the left sidebar, click **Pages**

4. Under **Source**, select:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/docs`

5. Click **Save**

6. Wait 1-2 minutes for GitHub to build your site

7. Your landing page will be live at:
   **https://rohannorden2121.github.io/FungiMap/**

---

## 📸 Step 2: Add Images

Your landing page needs 7 images. I've created placeholder references for all of them.

### Where to find images:
- **Unsplash**: https://unsplash.com (free, high-quality)
- **Pexels**: https://pexels.com (free stock photos)
- **Pixabay**: https://pixabay.com (free images)

### Images you need:

1. **mycelium-network.jpg** - Search: "mycelium network", "fungal hyphae"
2. **dna-sequencing.jpg** - Search: "DNA sequencing abstract", "metagenomics"
3. **quality-control.jpg** - Search: "bioinformatics pipeline", "data workflow"
4. **abundance-chart.jpg** - Search: "microbiome chart", "species diversity graph"
5. **biodiversity-map.jpg** - Search: "biodiversity map", "ecological survey"
6. **fungal-microscopy.jpg** - Search: "fungal microscopy", "fungal spores"
7. **lab-setup.jpg** - Search: "molecular biology lab", "DNA extraction"

### How to add them:

1. Download images from Unsplash/Pexels using the search terms above
2. Rename them to match the filenames (e.g., `mycelium-network.jpg`)
3. Place them in: `/Users/rohannorden/My Code/mycology-project/docs/images/`
4. Commit and push:
   ```bash
   cd "/Users/rohannorden/My Code/mycology-project"
   git add docs/images/
   git commit -m "Add images to landing page"
   git push origin main
   ```

### Detailed image guide:
See `docs/images/README.md` for detailed specifications for each image.

---

## 🔗 Step 3: Update Links

Before sharing, update these placeholder links in `docs/index.html`:

1. **Medium Post link** (appears 3 times):
   - Line 23: `<a href="#" class="btn btn-secondary" target="_blank">Medium Post</a>`
   - Line 146: `<a href="#" class="btn btn-secondary" target="_blank">Medium Blog Post</a>`
   - Line 170: `<a href="#" target="_blank">Medium</a>`
   
   Replace `#` with your actual Medium post URL

2. **Contact email** (line 173):
   - `<a href="mailto:your.email@example.com">Contact</a>`
   
   Replace `your.email@example.com` with your actual email

---

## ✨ Features of Your Landing Page:

✅ **Particles.js animation** - Interactive network background (like mycelium!)
✅ **Responsive design** - Works on mobile, tablet, and desktop
✅ **Smooth animations** - Sections fade in as you scroll
✅ **Your exact text** - Uses all the wording you provided
✅ **Professional styling** - Clean, modern design for admissions officers
✅ **GitHub integration** - Links to your repository and README

---

## 🎨 Optional Customization:

If you want to change colors, fonts, or layout:
- Edit `docs/style.css` (all styling is here)
- Edit `docs/index.html` (all content and structure)
- Edit `docs/script.js` (animations and interactions)

---

## 🧪 Test Your Landing Page Locally:

1. Open the file in your browser:
   ```bash
   open "/Users/rohannorden/My Code/mycology-project/docs/index.html"
   ```

2. Or use a local server:
   ```bash
   cd "/Users/rohannorden/My Code/mycology-project/docs"
   python3 -m http.server 8000
   ```
   Then visit: http://localhost:8000

---

## 📝 Files Created:

- `docs/index.html` - Main landing page
- `docs/style.css` - All styling and design
- `docs/script.js` - Particles animation and interactions
- `docs/images/README.md` - Image specifications and search terms

---

## 🎯 Next Steps:

1. ✅ Enable GitHub Pages (see Step 1 above)
2. 📸 Add images (see Step 2 above)
3. 🔗 Update Medium post and email links (see Step 3 above)
4. 🚀 Share your landing page URL in college applications!

---

## Need Help?

If you run into any issues:
1. Check that GitHub Pages is enabled correctly
2. Wait a few minutes after pushing changes
3. Clear your browser cache if you don't see updates
4. Check the Actions tab on GitHub to see build status

Your landing page URL will be:
**https://rohannorden2121.github.io/FungiMap/**

Good luck with your applications! 🎓