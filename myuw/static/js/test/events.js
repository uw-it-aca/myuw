var ec = require("../card/events.js"),
    assert = require("assert");
moment = require("../../vendor/js/moment.2.8.3.min.js");

describe('EventsCard', function(){
    describe('group_by_date', function(){
        var events = JSON.parse("[{\"start\": \"2013-04-1610: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D110608069\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Asst.Prof.AlexanderStatsyuk\"    },    {\"start\": \"2013-04-1618: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D110608069\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Steve\"    },    {\"start\": \"2013-04-1716: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D110741160\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Prof.MatthewBecker\"    },    {\"start\": \"2013-04-1916: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D113278967\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Assoc.Prof.RyanShenvi\"    },    {\"start\": \"2013-04-1916: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D113278967\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Assoc.Prof.RyanShenvi\"    },    {\"start\": \"2013-04-1916: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D113278967\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Assoc.Prof.RyanShenvi\"    },    {\"start\": \"2013-04-1916: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D113278967\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Assoc.Prof.RyanShenvi\"    },    {\"start\": \"2013-04-1916: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D113278967\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Assoc.Prof.RyanShenvi\"    },    {\"start\": \"2013-04-1916: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D113278967\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Assoc.Prof.RyanShenvi\"    },    {\"start\": \"2013-04-1916: 00: 00-07: 00\",\"event_url\": \"http: //www.washington.edu/calendar/?trumbaEmbed=view%3Devent%26eventid%3D113278967\",\"event_location\": \"ChemistryBuilding(CHB)\",\"summary\": \"OrganicChemistrySeminar: Assoc.Prof.RyanShenvi\"}]");
        it('should sort events', function(){
            var data = ec.EventsCard.group_by_date(events);
            var shown = data[0];
            var hidden = data[1];
            assert.equal(hidden.length, 4);
            assert.equal(shown.length, 6);
        });
    });

});
