from ..models import User
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status

class DenunciateUser:
    def __init__(self, user_who_reported, user_reported_id):
       self.user_who_reported = user_who_reported
       self.set_user_reported(user_reported_id)

    def set_user_reported(self, user_reported_id):
        try:
            self.user_reported = User.objects.filter(id=user_reported_id).first()
        except User.DoesNotExist:
            return Response({'message': 'Usuario no encontrado'})

    def start_denunciate_proccess(self):
        try:
            is_complaint_valid = self.verify_complain()
        except Exception as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        
        if is_complaint_valid:
            self.add_complaint()
            user_reported_denuncations = self.count_user_reported_complaints()
            if user_reported_denuncations >= 20:
                self.send_complaint_mail(user_reported_denuncations=user_reported_denuncations)
    
    def verify_complain(self):
        if self.user_reported not in self.user.denunciations.all():
            if self.user_reported != self.user_who_reported:
                raise Exception('No te puedes denunciar a ti mismo')
        return Exception('Usuario ya denunciado')
    
    def add_complaint(self):
        self.user_reported.denunciations.add(self.user_who_reported)

    def count_user_reported_complaints(self) -> int:
        user_reported_denuncations = len(self.user_reported.denunciations.all())
        return user_reported_denuncations
    
    def send_complaint_mail(self, user_reported_denuncations):
        send_mail("Exceso de denuncias", f"El usuario ha sido denunciado {user_reported_denuncations} veces", 
                  None,  ["jackson0102almeida@gmail.com"])




"""
try:
      user_id = request.data['id']
      user = User.objects.filter(id=user_id).first()

      if user not in user.denunciations.all():
        if user != request.user:
          user.denunciations.add(request.user)

          user_denuncations = len(user.denunciations.all())
          if user_denuncations >= 20:
              send_mail("Exceso de denuncias", f"El usuario ha sido denunciado {user_denuncations} veces", None,  ["jackson0102almeida@gmail.com"])

          return Response({
              'message': 'Usuario denunciado'
          }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'No te puedes denunciar a ti mismo'
            })
      else:
          return Response({
              'message': 'Usuario ya denunciado'
          })
    
    except User.DoesNotExist:
        return Response({
            'message': 'Usuario no encontrado'
        })"""