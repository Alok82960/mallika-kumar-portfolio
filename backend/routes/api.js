const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const multer = require('multer');
const path = require('path');
const rateLimit = require('express-rate-limit');
const Portfolio = require('../models/Portfolio');
const Contact = require('../models/Contact');

// Configure rate limiters
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // Limit each IP to 5 login requests per `window`
  message: { msg: 'Too many login attempts, please try again after 15 minutes' }
});

const contactLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // Limit each IP to 5 contact requests per `window`
  message: { msg: 'Too many messages sent, please try again later' }
});

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, '../uploads/'));
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + path.extname(file.originalname));
  }
});
const upload = multer({ storage: storage });

// Middleware to verify JWT token from HttpOnly cookie
const auth = (req, res, next) => {
  const token = req.cookies.token;
  if (!token) return res.status(401).json({ msg: 'No token, authorization denied' });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (e) {
    res.status(400).json({ msg: 'Token is not valid' });
  }
};

// @route   POST /api/login
// @desc    Authenticate admin & get token in cookie
router.post('/login', loginLimiter, async (req, res) => {
  const { password } = req.body;
  if (!password) {
    return res.status(400).json({ msg: 'Please enter a password' });
  }

  try {
    // Check password against bcrypt hash in env variable
    const isMatch = await bcrypt.compare(password, process.env.ADMIN_PASSWORD_HASH);
    
    if (isMatch) {
      const payload = { user: { id: 'admin' } };
      jwt.sign(
        payload,
        process.env.JWT_SECRET,
        { expiresIn: '24h' },
        (err, token) => {
          if (err) throw err;
          // Set JWT in HttpOnly cookie
          res.cookie('token', token, {
            httpOnly: true,
            secure: process.env.NODE_ENV === 'production',
            sameSite: 'strict',
            maxAge: 24 * 60 * 60 * 1000 // 24 hours
          });
          res.json({ msg: 'Logged in successfully' });
        }
      );
    } else {
      res.status(400).json({ msg: 'Invalid Credentials' });
    }
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
});

// @route   POST /api/logout
// @desc    Clear cookie
router.post('/logout', (req, res) => {
  res.clearCookie('token');
  res.json({ msg: 'Logged out' });
});

// Default data if DB is empty
const defaultData = {
  positions: [
    {icon:'fa-chart-line',title:'Head, Research Council',org:'World Cooperative Economic Forum (WCoopEF)'},
    {icon:'fa-people-arrows',title:'Member, Committee for Cooperatives in Education',org:'International Cooperative Alliance - Asia Pacific'},
    {icon:'fa-landmark',title:'Member, Uttarakhand Cooperative Policy Committee',org:'Cooperatives Department, Government of Uttarakhand'},
    {icon:'fa-venus',title:'Special Invitee, Gender Analysis & Budget',org:'Ministry of Women & Child Development, Govt. of India'}
  ],
  experience: [
    {year:'2025',title:'Speaker, VNR Lab on SDG 5: Gender Equality',place:'High-Level Political Forum, UN HQ, New York',desc:'Addressed the contribution of cooperatives in advancing women empowerment and inclusive development.'},
    {year:'2025',title:'Women Achiever Award & Romasha Award',place:'New Delhi, India',desc:'Received Women Achiever Award from Attorney General of India (Mar 8) and Romasha Award from Chairman IFFCO (May 6) for Cooperative Education Framework.'}
  ],
  publications: [
    {title:'The Future of Work Post Covid-19: Key Perceived HR Implications of Hybrid Workplaces in India',source:'Journal of Management Development',year:'2022',tag:'scopus',tagLabel:'SCOPUS'}
  ],
  awards: [
    {icon:'fa-medal',title:'Romasha Award 2025',year:'May 6, 2025',desc:'Conferred by Shri Dileep Sanghani, Chairman IFFCO, for profound contribution to the Cooperative Education Framework.'}
  ],
  mous: [
    {partner:'SRCC & Metropolitan College of New York (MCNY)',country:'United States',flag:'fa-flag-usa',date:'Sep 27, 2014'}
  ],
  gallery: [],
  profilePhoto: null,
  editable: {},
  socials: []
};

// @route   GET /api/data
// @desc    Get portfolio data
router.get('/data', async (req, res) => {
  try {
    let portfolio = await Portfolio.findOne();
    if (!portfolio) {
      // Create default
      portfolio = new Portfolio(defaultData);
      await portfolio.save();
    }
    res.json(portfolio);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   PUT /api/data
// @desc    Update portfolio data
router.put('/data', auth, async (req, res) => {
  try {
    const data = req.body;
    let portfolio = await Portfolio.findOne();
    if (!portfolio) {
      portfolio = new Portfolio(data);
    } else {
      Object.assign(portfolio, data);
    }
    await portfolio.save();
    res.json(portfolio);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   POST /api/upload
// @desc    Upload file(s)
router.post('/upload', auth, upload.array('files', 10), (req, res) => {
  try {
    const fileUrls = req.files.map(file => `/uploads/${file.filename}`);
    res.json({ urls: fileUrls });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route   POST /api/contact
// @desc    Submit contact form
router.post('/contact', contactLimiter, async (req, res) => {
  try {
    const { name, email, subject, message } = req.body;
    const newContact = new Contact({ name, email, subject, message });
    await newContact.save();
    res.json({ msg: 'Message received' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router;
