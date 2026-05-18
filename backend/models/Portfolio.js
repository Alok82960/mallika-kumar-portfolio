const mongoose = require('mongoose');

const PortfolioSchema = new mongoose.Schema({
  positions: [{
    icon: String,
    title: String,
    org: String
  }],
  experience: [{
    year: String,
    title: String,
    place: String,
    desc: String
  }],
  publications: [{
    title: String,
    source: String,
    year: String,
    tag: String,
    tagLabel: String
  }],
  awards: [{
    icon: String,
    title: String,
    year: String,
    desc: String
  }],
  mous: [{
    partner: String,
    country: String,
    flag: String,
    date: String
  }],
  gallery: [{
    src: String,
    caption: String
  }],
  profilePhoto: String,
  editable: {
    type: Map,
    of: String,
    default: {}
  },
  socials: [String]
});

module.exports = mongoose.model('Portfolio', PortfolioSchema);
