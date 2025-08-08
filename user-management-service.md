``` db
users [icon: user, color: blue] {
  id                     string pk
  username               string
  email                  string unique
  password(hash)         string
  role                   enum("student", "mentor", "admin")
  isEmailVerified        boolean
  oauthProvider          enum("google", "github", "facebook")
  oauthId                string
  referredBy             string fk  
  createdAt              timestamp 
  updatedAt              timestamp
  lastLogin              timestamp
  isActive               boolean
  deletedAt              timestamp
}


user_profile[icon:user, color:blue]{
 id                     string pk
 userId                 string fk
  firstName              string
  Lastname               string
 skills                 string[]
 education              string[]
 about                  string
  bio                    string
  phone                  string unique
  profileImage           string
}


mentor_profiles [icon: briefcase, color: green] {
  id                     string pk
  userId                 string fk
  verifiedStatus         enum("pending", "approved", "rejected")
  verificationNote       string
  about                  string
  hourlyRate             number
  totalSessionsConducted number default(0)
  averageRating          number default(0)
  reviewCount            number default(0)
  isAvailable            boolean
  hiringCardUrl          string
  createdAt              timestamp
  updatedAt              timestamp
}

<!-- Source of truth -->
mentor_availability [icon: calendar, color: purple] {
  id                     string pk
  mentorId / (userId)    string fk
  dayOfWeek              enum("sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday")
  startTime              time
  endTime                time
  timezone               string
  isRecurring            boolean default(true)
  createdAt              timestamp
  updatedAt              timestamp
}

categories [icon: tag, color: orange] {
  id                     string pk
  name                   string unique
  description            string
  createdAt              timestamp
  updatedAt              timestamp
}

subjects [icon: layers, color: yellow] {
  id                     string pk
  categoryId             string fk
  name                   string unique
  description            string
  createdAt              timestamp
  updatedAt              timestamp
}

mentor_subjects [icon: link, color: green] {
  id                     string pk
  mentorId               string fk
  subjectId              string fk
}

reviews [icon: star, color: yellow] {
  id                     string pk
  mentorId               string fk
  userId                 string fk
  rating                 number min(1) max(5)
  totalReview            number
  comment                text
  reviewStatus           enum("visible", "flagged", "hidden")
  createdAt              timestamp
}


mentorship_plans [icon: diamond, color: teal] {
  id                   string pk
  mentorId             string fk
  title                string
  litePrice            number
  standardPrice        number
  proPrice             number
  liteDescription      string
  standardDescription  string
  proDescription       string 
  callLimitPerMonth    number
  chatSupport          boolean
  responseTime         string
  handsOnSupport       boolean
  isActive             boolean default
  createdAt            timestamp
  updatedAt            timestamp
}

mentorship_sessions [icon: clock, color: blue] {
  id                   string pk
  mentorId             string fk
  title                string
  description          text
  hourlyRate           number
  durationMinutes      number
  sessionType          enum("video_call", "chat", "in_person")
  isActive             boolean default(true)
  createdAt            timestamp
  updatedAt            timestamp
}

# Relationships
users.id > mentor_profiles.userId
users.id > mentor_availability.mentorId
users.id > reviews.studentId
mentor_profiles.id > reviews.mentorId
categories.id > subjects.categoryId
subjects.id > mentor_subjects.subjectId
mentor_profiles.id > mentor_subjects.mentorId
mentor_profiles.id > mentorship_plans.mentorId
mentor_profiles.id > mentorship_sessions.mentorId
users.id > users.referredBy




# User and Mentor Schema
This document describes the database schema for users and mentors in the eraser.io application.
mentor_profiles.userId > mentor_subjects.mentorId
mentor_profiles.userId > mentorship_plans.mentorId
mentor_profiles.userId > mentorship_sessions.mentorId

```





