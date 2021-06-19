# Introduction
In the past year, a deadly virus has taken over the entire United States. The government has failed to give us the information we all need and as a consequence, many people have denied that it's even happening. If left unchecked, the consequences could be disastrous. I'm talking, of course, about UFO fever.

That's right, with the official Pentagon report on UFO's right around the corner, and the hype building, I think it's an appropriate time to examine one of the oldest and largest collections of UFO reports on the internet: the National UFO Reporting Center database.

So let's go for the biggest question of all: What are all these lights in the sky? Can we truly attribute all sightings to tricks of the light, man made aircraft, and oddly shaped clouds? Or are we in the midst of an interplanetary invasion?

# Summary
To start with, I've broken the analysis down into three questions, the answers to which give some idea as to what causes UFO reports. These answers won't cover everything, as that would involve a much larger and more in depth data set, but we can at least find correlations between some variables to give us a general idea of what's behind UFO sightings. The questions are as follows:

1. When have there been spikes in UFO activity?
2. How have UFO reports changed over time?
3. Do more UFO sightings happen during day time or night time?
4. (Bonus) What state has the most UFO reports per capita?

Before we start, a couple of notes. First of all each question is broken down into two sections; namely: methodology and results. Second, much of the approaches I took to these questions won't be reflected in the notebook. I made the final plots from plots that I used to find the trends, and as a result the initial plots are not present in the notebook. I also did quite a lot of refactoring. Ultimately I should have been committing those changes to this repository each time, but alas it is far too late to change that now.

## Question 1. When have there been spikes in UFO activity?
##### Methodology:
My approach to answering this question was pretty simple. I found the cumulative reports for each day of the year across every year, and plotted them a month at a time. Whenever I found a spike I would look at that month in each year to see if it was a one-time spike or an annual event. If it was the former, the final plot would simply be the report count for each day in the month for that year. If it was the latter, the final plot would show the average reports for each day in the month across all years since 2000.

##### Results:
In all, I found one spike related to an annual event and one related to a one off event. The annual event was, quite entertainingly, the 4th of July. The one time event appears to be a U.S. Navy missile launch on November 7th of 2015. The plots for both spikes are below.

INSERT IMAGES HERE PLEASE

## Question 2. How have UFO reports changed over time?
##### Methodology:
This was another relatively simple question. To answer this, I took two approaches. First, I simply plotted the amount of reports for each year. There was already a very convenient year column in the NUFORC data set, so all I really had to do was make a histogram of that column. As you'll see I limited the plot to a period of 60 years, from 1956 to 2016. The upper limit was due to the fact that the dataset I used was scraped from NUFORC's website in early 2017, meaning that a count of the UFO reports for that year wouldn't have been useable. The lower limit was decided on simply because NUFORC was founded in 1974, and therefore reports before that date are sparse at best and all retroactively added. I believed this would have added junk to the chart without providing reliable information.

Second, I decided to take a detailed look at how many reports were made each month. Specifically, I wanted to look at each month's total UFO reports for each year individually. I also wanted to see if there were months that were typically more or less active. To communicate this visually, I decided to use an animation. 

The first part of the animation involved the counts for each year. As the years went on, these counts would be layered over each other, one after the other. However, the counts alone didn't work. As we've seen, UFO sightings have been increasing year over year. To account for this, I decided to express each month's sightings as the percentage of the year's sightings that took place within that month. This made each year's trend comparable. The second part of the animation simply highlights the minimum and maximum value for each month from 2000-2016. Of note is that I filtered out the 4th of July to ensure that July wouldn't obscure the overall trend.

##### Results:
The amount of UFO sightings per year appears to have increased exponentially over time. However, scaling the y-axis accordingly shows us that reports were actually happening at a pretty consistent rate before the mid-90's. I believe the reason for this is the popularization of cell phones and the internet making it much easier to report these sightings. That is surely not the only variable, and I, of course, can only speculate, but if pressed for an explanation, that is what I would go with.

As for the reports per month, it seems that the latter half of the year accounts for more reports than the former. I expect this is for multiple reasons. Firstly, late Spring and Summer is when people usually spend the most time outside. A likely explanation for the rest of the year is that many people are travelling for the holidays. Both of these explanations would make it more likely for people to experience UFO encounters. However, again, there could be many explanations for this trend, and I can only speculate as to what they would be.

INSERT IMAGES HERE PLEASE

## Question 3. Do more UFO sightings happen during day time or night time?
##### Methodology:
The first thing I wanted to have was a plot that compared the amount of sightings when the sun was up to the amount of sightings when the sun was down. To do this, I needed to assign either "day" or "night" to each sighting. This is difficult because there is no set time that day turns to night. It changes based on location and time of year. That meant that whatever solution I used had to account for those factors as well.

To accomplish this, I used the library PyEphem. Using Ephem, I could create "observers" which have spherical coordinates, date and timestamps, and altitudes associated with them. Using those values, Ephem could calculate the altitude of the Sun relative to the observer. If the altitude was negative, that meant that the sun was below the horizon, and therefore it was nighttime.

However, there were more than a few challenges associated with creating these observers. Firstly, the reports themselves didn't come with latitudes and longitudes. What they did come with were cities. So, I found a dataset containing the coordinates for over 28,000 U.S. cities, created an observer for each city using the city's coordinates, and joined those observers to the sightings using the city and state as a key. If the city the sighting took place in didn't appear in the cities dataset, the most populated city for the state that the sighting took place in was used as a substitute. Reports that didn't have a state associated with them were dropped.

Secondly, Ephem uses UTC timestamps exclusively, while the timestamps for the sightings were in local time. Luckily, that same cities data set also came with time zones. So, I used the time zone for each city to convert the sighting timestamps to UTC.

Once both of these problems had been solved, I finally got what I believe to be a very accurate assessment of the time of day for each sighting. Of course it's not perfect; it doesn't take into account altitude for example. But it is, at the very least, more accurate than an arbitrary cutoff point would have been.

The next thing I wanted was a plot that determined how many sightings occurred in each hour of the day. This was mostly to confirm what I found with the first plot, but ended up being fairly interesting as well. Of course, this plot was much simpler as I just made a histogram using the hour column. What does need to be discussed here is the coloring of the histogram. I decided that I wanted to make a gradient as a rough way to visually depict the visibility at that hour. 

However, a simple gradient from the center wasn't going to cut it, so instead I made two gradients. The first faded from a dark purple to yellow, and ended at what I could find on the internet was the hour in which latest sunrise of the year occurred in the United States. I did the opposite for the tail of the plot, using the earliest sunset. Between the latest sunrise and earliest sunset, I left the bars entirely yellow, as a way of showing that at no point were any of the sightings that took place within those hours during the night time.

##### Results:
As is shown in the first plot, the overwhelming majority of sightings (~79%), take place at night. We can also see that there is an incredibly smooth relationship between how deep into night an hour is and how many sightings occur within that hour; especially if you account for the typical period a person is expected to be asleep. Even more satisfying is the degree to which sightings during sunny hours remain consistent.

INSERT IMAGES HERE PLEASE

## Bonus Question. What state has the most UFO reports per capita?
##### Methodology:
For this question, I used census data to divide the amount of sightings in each state by their respective populations. I then plotted these sightings from highest to lowest. There's not much more to say about this question, except to explain why I didn't include it in the final article. From a methodology standpoint, I didn't know if this was an appropriate way to go about measuring reports per capita. The sightings take place over multiple years, but the population measures are estimates from 2019. I didn't feel confident that any trend I found would be reliable, which brings me to the results.

##### Results:
As you can see, there isn't really a strong trend here, at least, not on the surface. Though Washington does have the most sightings per capita, looking at the x-axis there isn't much of a difference between any state. Puerto Rico has the lowest, however that is mostly due to the fact that there are only 36 reports from Puerto Rico in the dataset. What's more, the plot is very clumsy, with the y-axis being almost illegible. Overall, there was really nothing worthy of reporting here, however, I left it in because I personally find it fun. I also did want to comment that their rankings on this plot seem roughly opposite to their rankings in population density, though that is only a comment, not a claim.

INSERT IMAGES HERE PLEASE

# Sources
- UFO Reports: http://www.nuforc.org/ though I used this dataset generated from nuforc instead of getting it directly https://data.world/khturner/national-ufo-reporting-center-reports
- Cities data: https://simplemaps.com/data/us-cities
- Latest Sunrise and Earliest Sunset: https://abc7ny.com/winter-solstice-latest-sunrise-earliest-sunset-solar-time/8593291/#:~:text=However%2C%20the%20earliest%20sunset%20date,2021%20at%207%3A20%20a.m.
- State Population Data (I cleaned it up myself in google sheets): https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html
- Various: https://www.wikipedia.org

------------------------------------------------------------------------