# Vercel Deployment Guide

## Prerequisites
- Vercel account (you already have one at https://vercel.com/hamzaans-projects)
- Git repository with your code

## Deployment Steps

### 1. Install Vercel CLI (if not already installed)
```bash
npm i -g vercel
```

### 2. Login to Vercel
```bash
vercel login
```

### 3. Deploy to Vercel
```bash
vercel
```

### 4. Follow the prompts:
- Set up and deploy: `Y`
- Which scope: Select your account
- Link to existing project: `N`
- Project name: `referral-app` (or your preferred name)
- Directory: `./` (current directory)
- Override settings: `N`

### 5. For production deployment:
```bash
vercel --prod
```

## Troubleshooting Deployment Errors

### NOT_FOUND Errors
If you encounter a "NOT_FOUND" error during deployment:

1. **Check the build logs** in the Vercel dashboard for specific error messages
2. **Verify file structure** - ensure all files are in the correct location
3. **Check Python version** - Vercel supports Python 3.9+
4. **Verify dependencies** - all packages in requirements.txt should be compatible
5. **Check the wsgi.py file** - this is the entry point for Vercel

### FUNCTION_INVOCATION_FAILED Errors (500 Internal Server Error)
If you encounter a "FUNCTION_INVOCATION_FAILED" error:

1. **Check function logs** in the Vercel dashboard
2. **Database issues**: The app now uses in-memory database for Vercel
3. **Import errors**: Check for missing dependencies
4. **Memory issues**: The simplified app uses less memory

### Common Solutions:
- **Clear Vercel cache**: Delete the `.vercel` folder and redeploy
- **Check build output**: Look for any import errors or missing dependencies
- **Verify routes**: Ensure the vercel.json routing is correct
- **Use simplified app**: The app_simple.py is optimized for serverless deployment

## Important Notes

### Database Considerations
- Vercel uses serverless functions, so the SQLite database will be read-only
- For production, consider using a cloud database like:
  - **Vercel Postgres** (recommended for Vercel)
  - **PlanetScale**
  - **Supabase**
  - **Railway**

### Environment Variables
If you need to add environment variables later:
```bash
vercel env add DATABASE_URL
```

### Custom Domain
After deployment, you can add your custom domain in the Vercel dashboard:
1. Go to your project in Vercel dashboard
2. Click on "Settings" → "Domains"
3. Add your domain: `referrals.hansari.org`

## Benefits of Vercel Deployment
- ✅ No more IP address issues
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Automatic deployments from Git
- ✅ Serverless scaling
- ✅ Built-in analytics

## Migration from Self-Hosted
1. Deploy to Vercel
2. Update your domain DNS to point to Vercel
3. Stop your local server
5. Enjoy worry-free hosting!
