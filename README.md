# 🏰 Random Fort Generator

> Display a random historic Maharashtra fort on your GitHub profile README - changes on every page refresh!

![Random Fort Card](https://your-app-url.vercel.app/api/fort-card.svg)

## ✨ Features

- 🏰 **228 Historic Forts** from Maharashtra
- 🔄 **Random on Refresh** - Each page load shows a different fort
- 📸 **Beautiful SVG Cards** - Dark theme with fort images and descriptions
- 📍 **Location Badges** - Shows the location of each fort
- ⚡ **Fast & Free** - Deploy on Vercel for free hosting

## 🎴 Card Display

Each card shows:
- **Image** - Fort photograph
- **Name** - Fort name
- **About** - Brief description of the fort
- **Location** - Where the fort is located

## 🚀 Quick Start

### Add to Your GitHub README

```markdown
<a href="https://your-app-url.vercel.app">
  <img src="https://your-app-url.vercel.app/api/fort-card.svg" alt="Random Fort" />
</a>
```

### Deploy Your Own

1. **Fork this repository**

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your forked repository
   - Deploy (no configuration needed!)

3. **Update your README** with your Vercel URL

## 🔗 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/fort-card.svg` | Random fort as SVG card (use in README) |
| `/api/fort` | Random fort JSON data |
| `/api/fort/{id}` | Specific fort SVG (0-227) |
| `/api/all-forts` | All forts JSON data |

## 🏛️ Forts Collection

The collection includes 228 historic forts from Maharashtra including:

- **Pune District** - Sinhagad, Rajgad, Torna, Lohagad, Shivneri, and more
- **Raigad District** - Raigad, Murud-Janjira, Kolaba, Karnala, and more
- **Satara District** - Pratapgad, Sajjangad, Ajinkyatara, and more
- **Kolhapur District** - Panhala, Vishalgad, Rangana, and more
- **Sindhudurg District** - Sindhudurg, Vijaydurg, and more
- **Nashik District** - Salher, Mulher, Harihar, and more
- **And many more districts...**

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Visit http://localhost:8081
```

## 📝 License

MIT License - Feel free to use and modify!

---

Made with ❤️ for Maharashtra Heritage
