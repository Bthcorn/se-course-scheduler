
import streamlit as st
from web.views.base_page import BasePage


class SchedulesPage(BasePage):

    def render(self):
        st.title("Recommended Schedules")
        
        schedule_generated = st.session_state.get("schedule_generated", False)
        
        if not schedule_generated:
            st.info("No schedules generated yet. Please generate schedules from the Dashboard.")
            st.markdown("---")
            st.subheader("Room Availability (All Rooms)")
            self.render_all_rooms_availability()
            return
        
        result = st.session_state.get("schedule_result", {})
        if not result or "schedules" not in result:
            st.warning("No schedule data available")
            return
        
        schedules = result["schedules"]
        
        tab1, tab2 = st.tabs(["📅 Year-wise Schedules", "🏢 Room-wise Schedules & Availability"])
        
        with tab1:
            self.render_year_wise_schedules(schedules)
        
        with tab2:
            self.render_room_wise_schedules(schedules)
    
    def render_all_rooms_availability(self):
        rooms_query = "room(RoomID, Capacity)"
        all_rooms = list(self.scheduler.prolog.query(rooms_query))
        
        if not all_rooms:
            st.warning("No rooms found")
            return
        
        reserved_query = "reserved(Room, Day, TimeSlot, Reason)"
        reserved_slots = list(self.scheduler.prolog.query(reserved_query))
        
        for room_data in sorted(all_rooms, key=lambda x: str(x["RoomID"])):
            room_id = str(room_data["RoomID"])
            
            st.markdown(f"### Room {room_id.upper()}")
            
            room_reserved = [r for r in reserved_slots if str(r["Room"]) == room_id]
            
            availability_table = self.create_availability_table(
                room_id, [], room_reserved
            )
            
            st.markdown(availability_table, unsafe_allow_html=True)
            st.markdown("---")

    
    def render_year_wise_schedules(self, schedules):
        st.subheader("Year-wise Weekly Schedules")
        
        years = sorted(set(int(data["year"]) for data, _ in schedules))
        
        for year in years:
            st.markdown(f"### Year {year} - Weekly Schedules")
            
            year_schedules = [(data, flag) for data, flag in schedules if int(data["year"]) == year]
            
            schedule_table = self.create_schedule_table(year_schedules)
            
            if schedule_table:
                st.markdown(schedule_table, unsafe_allow_html=True)
            else:
                st.info(f"No courses scheduled for Year {year}")
            
            st.markdown("---")
    
    def render_room_wise_schedules(self, schedules):
        st.subheader("Room-wise Schedules & Availability")
        
        rooms_query = "room(RoomID, Capacity)"
        all_rooms = list(self.scheduler.prolog.query(rooms_query))
        
        if not all_rooms:
            st.warning("No rooms found")
            return
        
        reserved_query = "reserved(Room, Day, TimeSlot, Reason)"
        reserved_slots = list(self.scheduler.prolog.query(reserved_query))
        
        for room_data in sorted(all_rooms, key=lambda x: str(x["RoomID"])):
            room_id = str(room_data["RoomID"])
            
            st.markdown(f"### Room {room_id.upper()}")
            
            room_schedules = [(data, flag) for data, flag in schedules if data["room"] == room_id]
            
            room_reserved = [r for r in reserved_slots if str(r["Room"]) == room_id]
            
            availability_table = self.create_availability_table(
                room_id, room_schedules, room_reserved
            )
            
            st.markdown(availability_table, unsafe_allow_html=True)
            st.markdown("---")
    
    def create_availability_table(self, room_id, room_schedules, room_reserved):
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        time_slots = [
            ("Morning Session", "08:00 - 12:00", "morning"),
            ("After Session", "13:00 - 16:00", "afternoon"),
            ("Evening Session", "16:30 - 18:30", "evening")
        ]
        
        schedule_map = {}
        for data, flag in room_schedules:
            day = data["day"].capitalize()
            timeslot = data["timeslot"].lower()
            
            if timeslot == "morning":
                slot_name = "Morning Session"
            elif timeslot == "afternoon":
                slot_name = "After Session"
            elif timeslot == "evening":
                slot_name = "Evening Session"
            else:
                slot_name = timeslot
            
            key = (day, slot_name)
            if key not in schedule_map:
                schedule_map[key] = []
            schedule_map[key].append((data, flag))
        
        reserved_map = {}
        for reserved in room_reserved:
            day = str(reserved["Day"]).capitalize()
            timeslot = str(reserved["TimeSlot"]).lower()
            
            if timeslot == "morning":
                slot_name = "Morning Session"
            elif timeslot == "afternoon":
                slot_name = "After Session"
            elif timeslot == "evening":
                slot_name = "Evening Session"
            else:
                slot_name = timeslot
            
            key = (day, slot_name)
            reason = str(reserved["Reason"])
            reserved_map[key] = reason
        
        html = '<table style="width:100%; border-collapse: collapse; margin: 20px 0;">'
        
        html += '<thead><tr style="background-color: #f0f0f0;">'
        html += '<th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Day</th>'
        for slot_name, time_range, _ in time_slots:
            html += f'<th style="border: 1px solid #ddd; padding: 12px; text-align: center;">{slot_name}<br/><small>{time_range}</small></th>'
        html += '</tr></thead><tbody>'
        
        for day in days:
            html += '<tr>'
            html += f'<td style="border: 1px solid #ddd; padding: 12px; font-weight: bold;">{day}</td>'
            
            for slot_name, _, _ in time_slots:
                key = (day, slot_name)
                cell_style = "border: 1px solid #ddd; padding: 12px; text-align: center;"
                
                if key in schedule_map:
                    courses_html = []
                    for data, flag in schedule_map[key]:
                        course_name = data["course_name"]
                        professor = data["professor"]
                        
                        if flag == "preference_not_met":
                            bg_color = "#ffcccc"
                            course_html = f'<div style="background-color: {bg_color}; padding: 8px; margin: 4px 0; border-radius: 4px;">'
                        else:
                            bg_color = "#e8f5e9"
                            course_html = f'<div style="background-color: {bg_color}; padding: 8px; margin: 4px 0; border-radius: 4px;">'
                        
                        course_html += f'<strong>{course_name}</strong><br/>'
                        course_html += f'{professor}'
                        course_html += '</div>'
                        courses_html.append(course_html)
                    
                    html += f'<td style="{cell_style}">{"".join(courses_html)}</td>'
                
                elif key in reserved_map:
                    reason = reserved_map[key]
                    cell_content = f'<div style="background-color: #ffe6cc; padding: 8px; border-radius: 4px;">'
                    cell_content += f'<strong>[RESERVED]</strong><br/>{reason}'
                    cell_content += '</div>'
                    html += f'<td style="{cell_style}">{cell_content}</td>'
                
                else:
                    cell_content = '<div style="background-color: #ccffcc; padding: 8px; border-radius: 4px; color: #666;">Available</div>'
                    html += f'<td style="{cell_style}">{cell_content}</td>'
            
            html += '</tr>'
        
        html += '</tbody></table>'
        
        return html

    
    def create_schedule_table(self, schedules):
        if not schedules:
            return None
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        time_slots = [
            ("Morning Session", "08:00 - 12:00"),
            ("After Session", "13:00 - 16:00"),
            ("Evening Session", "16:30 - 18:30")
        ]
        
        schedule_map = {}
        for data, flag in schedules:
            day = data["day"].capitalize()
            timeslot = data["timeslot"].capitalize()
            
            if timeslot == "Morning":
                slot_name = "Morning Session"
            elif timeslot == "Afternoon":
                slot_name = "After Session"
            elif timeslot == "Evening":
                slot_name = "Evening Session"
            else:
                slot_name = timeslot
            
            key = (day, slot_name)
            if key not in schedule_map:
                schedule_map[key] = []
            schedule_map[key].append((data, flag))
        
        html = '<table style="width:100%; border-collapse: collapse; margin: 20px 0;">'
        
        html += '<thead><tr style="background-color: #f0f0f0;">'
        html += '<th style="border: 1px solid #ddd; padding: 12px; text-align: left;">Day</th>'
        for slot_name, time_range in time_slots:
            html += f'<th style="border: 1px solid #ddd; padding: 12px; text-align: center;">{slot_name}<br/><small>{time_range}</small></th>'
        html += '</tr></thead><tbody>'
        
        for day in days:
            html += '<tr>'
            html += f'<td style="border: 1px solid #ddd; padding: 12px; font-weight: bold;">{day}</td>'
            
            for slot_name, _ in time_slots:
                key = (day, slot_name)
                cell_style = "border: 1px solid #ddd; padding: 12px; text-align: center;"
                
                if key in schedule_map:
                    courses_html = []
                    for data, flag in schedule_map[key]:
                        course_name = data["course_name"]
                        professor = data["professor"]
                        room = data["room"]
                        
                        if flag == "preference_not_met":
                            bg_color = "#ffcccc"
                            course_html = f'<div style="background-color: {bg_color}; padding: 8px; margin: 4px 0; border-radius: 4px;">'
                        else:
                            bg_color = "#e8f5e9"
                            course_html = f'<div style="background-color: {bg_color}; padding: 8px; margin: 4px 0; border-radius: 4px;">'
                        
                        course_html += f'<strong>{course_name}</strong><br/>'
                        course_html += f'{professor}<br/>'
                        course_html += f'<small>( Room {room.upper()} )</small>'
                        course_html += '</div>'
                        courses_html.append(course_html)
                    
                    html += f'<td style="{cell_style}">{"".join(courses_html)}</td>'
                else:
                    html += f'<td style="{cell_style}"></td>'
            
            html += '</tr>'
        
        html += '</tbody></table>'
        
        return html

