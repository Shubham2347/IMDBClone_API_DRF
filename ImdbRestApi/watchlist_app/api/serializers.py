from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform,Review

#ModelSerializer 
# ---> follow one in many relation ...eg one movie has many review ... use nested serlizer in movie like this.

class ReviewSerializer(serializers.ModelSerializer):
    #user update
    revview_user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Review
        # fields="__all__"
        exclude=("watchlist",)

class WatchListSerializer(serializers.ModelSerializer):
    reviews=ReviewSerializer(many=True,read_only=True)
    class Meta:
        model=WatchList
        fields='__all__'

class StreamPlatformSerializer(serializers.ModelSerializer):# notimp--> HyperlinkedModelSerializer for getting url 
    watchlist=WatchListSerializer(many=True,read_only=True)  
    class Meta:
        model=StreamPlatform
        fields='__all__'

     #nested serializer  --> watchlist var is related_name in models.py foreign key field 
     # --> one to many one stramplatform has many movies(watchkists)  
    # watchlist=WatchListSerializer(many=True,read_only=True)
               #Or notImp serializer relation --> for single field -->
    # watchlist=serializers.StringRelatedField(many=True,read_only=True)    
    #watchlist=serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="watch_detail") 
   




    # custom seralizer field
    '''
    len_name=serializers.SerializerMethodField()
    def get_len_name(self,object):
        return len(object.name)
    '''    


'''
serializers.serializer

class MovieSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField()
    description=serializers.CharField()
    active=serializers.BooleanField()

    def create(self,validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self,instance,validated_data):
        instance.name=validated_data.get('name',instance.name)
        instance.description=validated_data.get('description',instance.description)
        instance.active=validated_data.get('active',instance.active)
        instance.save()
        return instance
    

'''

    # VALIDATION
    #3 validators
'''
        name=serializers.CharField(validators=[name_length])
            def name_length(self,value):
                if len(value)<2:
                    raise serializer.ValidationError("nm is short")
             else:
                    return value    
'''
    #2 object level validation
'''
    def validate(self,data):
            if data['name']==data['description']:
                raise serializers.ValidationError("name and description should be different")
            else:
                return data
    '''

    #1 field level validation
'''
    def validate_name(self,value):
        if len(value)<2:
            raise serializers.ValidationError("name is too short")
        else:
            return value

            OR
         VALIDATORS
    '''