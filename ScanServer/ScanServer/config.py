# -*- coding: utf-8 -*- 
import os

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 's_e_c_r_e_t_k_e_y_h_u_c_t_f')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@47.115.30.24:3306/scanserver?charset=utf8"



config = {
    'development': DevelopmentConfig,
}
