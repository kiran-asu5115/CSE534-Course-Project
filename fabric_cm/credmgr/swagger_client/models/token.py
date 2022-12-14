# coding: utf-8

"""
    Fabric Credential Manager API

    This is Fabric Credential Manager API  # noqa: E501

    OpenAPI spec version: 1.0.2
    Contact: kthare10@unc.edu
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Token(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id_token': 'str',
        'refresh_token': 'str',
        'created_at': 'str'
    }

    attribute_map = {
        'id_token': 'id_token',
        'refresh_token': 'refresh_token',
        'created_at': 'created_at'
    }

    def __init__(self, id_token=None, refresh_token=None, created_at=None):  # noqa: E501
        """Token - a model defined in Swagger"""  # noqa: E501
        self._id_token = None
        self._refresh_token = None
        self._created_at = None
        self.discriminator = None
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.created_at = created_at

    @property
    def id_token(self):
        """Gets the id_token of this Token.  # noqa: E501

        Identity Token  # noqa: E501

        :return: The id_token of this Token.  # noqa: E501
        :rtype: str
        """
        return self._id_token

    @id_token.setter
    def id_token(self, id_token):
        """Sets the id_token of this Token.

        Identity Token  # noqa: E501

        :param id_token: The id_token of this Token.  # noqa: E501
        :type: str
        """
        if id_token is None:
            raise ValueError("Invalid value for `id_token`, must not be `None`")  # noqa: E501

        self._id_token = id_token

    @property
    def refresh_token(self):
        """Gets the refresh_token of this Token.  # noqa: E501

        Refresh Token  # noqa: E501

        :return: The refresh_token of this Token.  # noqa: E501
        :rtype: str
        """
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        """Sets the refresh_token of this Token.

        Refresh Token  # noqa: E501

        :param refresh_token: The refresh_token of this Token.  # noqa: E501
        :type: str
        """
        if refresh_token is None:
            raise ValueError("Invalid value for `refresh_token`, must not be `None`")  # noqa: E501

        self._refresh_token = refresh_token

    @property
    def created_at(self):
        """Gets the created_at of this Token.  # noqa: E501


        :return: The created_at of this Token.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this Token.


        :param created_at: The created_at of this Token.  # noqa: E501
        :type: str
        """
        if created_at is None:
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Token, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Token):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
