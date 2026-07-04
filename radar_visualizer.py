import serial
import pygame
import math
import sys
import re


arduino_port = "COM3"  
baud_rate = 9600

try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=0.01)
except Exception as e:
    print(f"❌ خطأ: لا يمكن الاتصال بالمنفذ {arduino_port}.")
    sys.exit()


pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 رادار الأردوينو الفوري - الاستجابة اللحظية 🚀")
clock = pygame.time.Clock()

BG_COLOR = (10, 20, 10)       
RADAR_GREEN = (0, 210, 0)     
GLOW_GREEN = (0, 50, 0)       
ALERT_RED = (255, 0, 0)       

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT - 50
RADIUS = 500

current_angle = 0
current_distance = 0
object_detected = False

def trigger_alarm_sound():
    if sys.platform == "win32":
        import winsound
        winsound.Beep(2000, 40) # تقصير مدة الصفارة لـ 40 ملي ثانية لتواكب السرعة اللحظية

running = True
while running:
    screen.fill(BG_COLOR)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
   
    if ser.in_waiting > 0:
        try:
            # قراءة كل المخزن المتراكم والتخلص منه، والوقوف على آخر سطر
            raw_lines = ser.read(ser.in_waiting).decode('utf-8', errors='ignore').split('\r\n')
            
            # أخذ آخر سطر مكتمل التكوين
            valid_line = ""
            for l in reversed(raw_lines):
                if l and ',' in l:
                    valid_line = l
                    break
            
            if valid_line:
                numbers = re.findall(r'\d+', valid_line)
                if len(numbers) >= 2:
                    temp_angle = int(numbers[0])
                    temp_dist = int(numbers[1])
                    
                    if (0 <= temp_angle <= 180) and (2 <= temp_dist <= 250):
                        current_angle = temp_angle
                        current_distance = temp_dist
                        
                      
                        if 4 <= current_distance <= 40:
                            object_detected = True
                            trigger_alarm_sound()
                        else:
                            object_detected = False
        except:
            pass 


    for r in [100, 200, 300, 400, RADIUS]:
        pygame.draw.circle(screen, RADAR_GREEN, (CENTER_X, CENTER_Y), r, 1)
    
    for angle_deg in [30, 60, 90, 120, 150]:
        rad = math.radians(angle_deg)
        x = CENTER_X + RADIUS * math.cos(rad)
        y = CENTER_Y - RADIUS * math.sin(rad)
        pygame.draw.line(screen, GLOW_GREEN, (CENTER_X, CENTER_Y), (x, y), 1)


    rad_angle = math.radians(current_angle)
    sweep_x = CENTER_X + RADIUS * math.cos(rad_angle)
    sweep_y = CENTER_Y - RADIUS * math.sin(rad_angle)
    pygame.draw.line(screen, RADAR_GREEN, (CENTER_X, CENTER_Y), (sweep_x, sweep_y), 3)

    
    if object_detected: 
        factor = (current_distance / 100.0) * RADIUS
        if factor > RADIUS: factor = RADIUS
        obj_x = CENTER_X + factor * math.cos(rad_angle)
        obj_y = CENTER_Y - factor * math.sin(rad_angle)
        pygame.draw.circle(screen, ALERT_RED, (int(obj_x), int(obj_y)), 12)
        pygame.draw.circle(screen, ALERT_RED, (int(obj_x), int(obj_y)), 22, 2)

    
    font = pygame.font.SysFont("Consolas", 24)
    angle_text = font.render(f"Angle: {current_angle}°", True, RADAR_GREEN)
    dist_text = font.render(f"Distance: {current_distance} cm", True, RADAR_GREEN)
    status_text = font.render("STATUS: ALERT!", True, ALERT_RED) if object_detected else font.render("STATUS: CLEAR", True, RADAR_GREEN)
    
    screen.blit(angle_text, (30, 30))
    screen.blit(dist_text, (30, 70))
    screen.blit(status_text, (30, 110))

    pygame.display.flip()
    clock.tick(60)

ser.close()
pygame.quit()
sys.exit()